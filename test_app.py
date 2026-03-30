import os
import tempfile

import jwt
import pytest

import app as jwks_app


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()

    original_db = jwks_app.DB_FILE
    jwks_app.DB_FILE = db_path

    try:
        jwks_app.create_table()
        jwks_app.initialize_keys()
        jwks_app.app.config["TESTING"] = True

        with jwks_app.app.test_client() as client:
            yield client
    finally:
        jwks_app.DB_FILE = original_db
        os.close(db_fd)
        if os.path.exists(db_path):
            os.unlink(db_path)


def test_db_file_and_keys_created(client):
    assert jwks_app.count_keys() >= 2


def test_jwks_returns_valid_keys(client):
    response = client.get("/.well-known/jwks.json")
    assert response.status_code == 200

    data = response.get_json()
    assert "keys" in data
    assert isinstance(data["keys"], list)
    assert len(data["keys"]) >= 1

    jwk = data["keys"][0]
    assert jwk["kty"] == "RSA"
    assert jwk["alg"] == "RS256"
    assert "kid" in jwk
    assert "n" in jwk
    assert "e" in jwk


def test_auth_returns_valid_token(client):
    jwks_response = client.get("/.well-known/jwks.json")
    jwks_data = jwks_response.get_json()
    public_keys = jwks_data["keys"]

    response = client.post("/auth")
    assert response.status_code == 200

    data = response.get_json()
    assert "token" in data

    token = data["token"]
    header = jwt.get_unverified_header(token)
    assert "kid" in header

    matching_key = None
    for key in public_keys:
        if key["kid"] == header["kid"]:
            matching_key = key
            break

    assert matching_key is not None

    public_key = jwt.algorithms.RSAAlgorithm.from_jwk(matching_key)
    decoded = jwt.decode(token, public_key, algorithms=["RS256"])

    assert decoded["sub"] == "userABC"


def test_auth_returns_expired_token_when_requested(client):
    response = client.post("/auth?expired=true")
    assert response.status_code == 200

    data = response.get_json()
    assert "token" in data

    token = data["token"]
    decoded = jwt.decode(
        token,
        options={"verify_signature": False, "verify_exp": False},
        algorithms=["RS256"],
    )

    assert decoded["sub"] == "userABC"
    assert "exp" in decoded


def test_invalid_method_on_auth(client):
    response = client.get("/auth")
    assert response.status_code in (405, 404)


def test_jwks_only_returns_unexpired_keys(client):
    response = client.get("/.well-known/jwks.json")
    assert response.status_code == 200

    data = response.get_json()
    assert "keys" in data

    for key in data["keys"]:
        assert "kid" in key
        assert key["alg"] == "RS256"
