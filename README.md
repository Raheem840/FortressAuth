# FortressAuth

A JWT-based authentication microservice built with FastAPI and SQLModel.

## Features
- User registration with bcrypt password hashing
- Login with enumeration-safe error responses (identical errors for wrong password vs. unknown email, to prevent account enumeration)
- JWT access tokens with expiry
- Protected routes via dependency-injected token verification
- Rate limiting on login to mitigate brute-force attacks

## Security decisions
- **Passwords are hashed with bcrypt**, never stored in plaintext or reversibly encrypted.
- **JWT payloads contain no sensitive data** (email only) since JWT payloads are readable, not encrypted — only the signature is protected.
- **Secrets are loaded from environment variables**, never hardcoded, to avoid leaking the signing key via version control.

## Setup
1. `python3 -m venv venv && source venv/bin/activate`
2. `pip install -r requirements.txt`
3. Create a `.env` file with `JWT_SECRET_KEY=<your-secret>`
4. `fastapi run`

## Future work
- OAuth2/SSO, MFA, refresh tokens