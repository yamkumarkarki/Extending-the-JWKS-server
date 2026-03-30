# 🔐 JWKS Server with SQLite

## 📌 Overview
This project implements a JSON Web Key Set (JWKS) server using Flask and SQLite.  
It generates JWT tokens and exposes public keys through a JWKS endpoint.

---

## 🚀 Features
- JWT authentication (`/auth`)
- JWKS endpoint (`/.well-known/jwks.json`)
- SQLite database for key storage
- Supports both valid and expired tokens
- Secure parameterized SQL queries
- Pytest test suite with ~97% coverage

---

## 📁 Project Structure
```text
Extending-the-JWKS-server/
├── app.py
├── test_app.py
├── requirements.txt
├── README.md
├── totally_not_my_privateKeys.db
├── gradebot.png
├── pytest.png

## 📁Results/Gradebot/pytest
┌────────────────────────────────┬────────┬─────────┬──────────────────────────────────────────────────────────┐
│              NAME              │ POINTS │ AWARDED │                          NOTES                           │
├────────────────────────────────┼────────┼─────────┼──────────────────────────────────────────────────────────┤
│ /auth valid JWT authN          │  15.00 │   15.00 │                                                          │
│ Valid JWK found in JWKS        │  20.00 │   20.00 │                                                          │
│ Database exists                │  15.00 │   15.00 │                                                          │
│ Database query uses parameters │  15.00 │   15.00 │                                                          │
│ Quality                        │  20.00 │   15.00 │ The code is generally well-structured, but could benefit │
│                                │        │         │ from improved organization, such as grouping related     │
│                                │        │         │ functions together.                                      │
│                                │        │         │ Best practices are mostly followed, but error handling   │
│                                │        │         │ for database operations is lacking, which could lead to  │
│                                │        │         │ unhandled exceptions.                                    │
│                                │        │         │ Readability is good, but adding docstrings to functions  │
│                                │        │         │ would enhance understanding.                             │
│                                │        │         │ Overall, the code quality is solid, but ensure that      │
│                                │        │         │ database queries are parameterized to prevent SQL        │
│                                │        │         │ injection, especially in the `insert_key` function.      │
│                                │        │         │ Consider using context managers for database connections │
│                                │        │         │ to ensure proper resource management.                    │
├────────────────────────────────┼────────┼─────────┼──────────────────────────────────────────────────────────┤
│                 objective_bose │ Grade: │  94.12% │                                                          │
└────────────────────────────────┴────────┴─────────┴──────────────────────────────────────────────────────────┘


platform darwin -- Python 3.14.3, pytest-8.3.3, pluggy-1.6.0 -- /Users/yamkumarkarkiicloud.com/Downloads/project2-jwks/venv/bin/python
cachedir: .pytest_cache
rootdir: /Users/yamkumarkarkiicloud.com/Downloads/project2-jwks
plugins: cov-5.0.0
collected 6 items                                                                                                                                                           

test_app.py::test_db_file_and_keys_created PASSED                                                                                                                     [ 16%]
test_app.py::test_jwks_returns_valid_keys PASSED                                                                                                                      [ 33%]
test_app.py::test_auth_returns_valid_token PASSED                                                                                                                     [ 50%]
test_app.py::test_auth_returns_expired_token_when_requested PASSED                                                                                                    [ 66%]
test_app.py::test_invalid_method_on_auth PASSED                                                                                                                       [ 83%]
test_app.py::test_jwks_only_returns_unexpired_keys PASSED                                                                                                             [100%]

---------- coverage: platform darwin, python 3.14.3-final-0 ----------
Name     Stmts   Miss  Cover   Missing
--------------------------------------
app.py      78      2    97%   115, 154
--------------------------------------
TOTAL       78      2    97%


============================================================================= 6 passed in 1.35s ===================================
