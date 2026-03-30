import base64
import sqlite3
import time

import jwt
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from flask import Flask, jsonify, request

DB_FILE = "totally_not_my_privateKeys.db"

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db_connection()
    conn.execute("""
    CREATE TABLE IF NOT EXISTS keys(
        kid INTEGER PRIMARY KEY AUTOINCREMENT,
        key BLOB NOT NULL,
        exp INTEGER NOT NULL
    )""")
    conn.commit()
    conn.close()


def generate_private_key_pem():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )


def count_keys():
    conn = get_db_connection()
    count = conn.execute("SELECT COUNT(*) FROM keys").fetchone()[0]
    conn.close()
    return count


def insert_key(pem, exp):
    conn = get_db_connection()
    conn.execute("INSERT INTO keys (key, exp) VALUES (?, ?)", (pem, exp))
    conn.commit()
    conn.close()


def initialize_keys():
    if count_keys() > 0:
        return

    now = int(time.time())
    insert_key(generate_private_key_pem(), now - 60)
    insert_key(generate_private_key_pem(), now + 3600)


def get_key(expired=False):
    conn = get_db_connection()
    now = int(time.time())

    if expired:
        row = conn.execute(
            "SELECT * FROM keys WHERE exp <= ? ORDER BY kid DESC LIMIT 1",
            (now,)
        ).fetchone()
    else:
        row = conn.execute(
            "SELECT * FROM keys WHERE exp > ? ORDER BY kid DESC LIMIT 1",
            (now,)
        ).fetchone()

    conn.close()
    return row


def load_private_key(pem):
    return serialization.load_pem_private_key(pem, password=None)


def int_to_base64url(n):
    byte_length = (n.bit_length() + 7) // 8
    data = n.to_bytes(byte_length, "big")
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")


def build_jwk(row):
    private_key = load_private_key(row["key"])
    public_key = private_key.public_key()
    numbers = public_key.public_numbers()

    return {
        "kty": "RSA",
        "kid": str(row["kid"]),
        "alg": "RS256",
        "use": "sig",
        "n": int_to_base64url(numbers.n),
        "e": int_to_base64url(numbers.e),
    }


@app.route("/auth", methods=["POST"])
def auth():
    expired = "expired" in request.args

    row = get_key(expired)
    if not row:
        return jsonify({"error": "no key"}), 500

    key = load_private_key(row["key"])
    now = int(time.time())

    payload = {
        "sub": "userABC",
        "iat": now,
        "exp": row["exp"] if expired else now + 300
    }

    token = jwt.encode(
        payload,
        key,
        algorithm="RS256",
        headers={"kid": str(row["kid"])}
    )

    return jsonify({"token": token})


@app.route("/.well-known/jwks.json")
def jwks():
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT * FROM keys WHERE exp > ?",
        (int(time.time()),)
    ).fetchall()
    conn.close()

    keys = [build_jwk(r) for r in rows]
    return jsonify({"keys": keys})


create_table()
initialize_keys()


if __name__ == "__main__":
    app.run(port=8080)
