from hashlib import sha256


def is_admin(token: str) -> bool:
    return token == sha256(b"admin").digest().hex()


def is_user(token: str) -> bool:
    return token == sha256(b"user").digest().hex()
