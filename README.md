# 🔐 JWKS Server with SQLite

## Overview
This project implements a JWKS server using Flask and SQLite.

## Features
- JWT authentication (`/auth`)
- JWKS endpoint (`/.well-known/jwks.json`)
- SQLite database for key storage
- Expired and valid key handling
- Test coverage ~97%

## Run
```bash
python app.py
