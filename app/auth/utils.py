from datetime import datetime, timedelta

import jwt
import bcrypt

from app.core.config import settings


def encode_jwt(
        payload: dict,
        private_key: str = settings.auth.private_key_path.read_text(),
        algorithm: str = settings.auth.algorithm,
        expire_minutes=settings.auth.access_token_expire_minutes,
):
    to_encode = payload.copy()
    now = datetime.now()
    expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(
        exp=expire,
        iat=now,
    )
    encoded = jwt.encode(
        payload=payload,
        key=private_key,
        algorithm=algorithm,
    )
    return encoded


def decode_jwt(
        token: str | bytes,
        public_key: str = settings.auth.public_key_path.read_text(),
        algorithm: str = settings.auth.algorithm,
):
    decode = jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=[algorithm]
    )
    return decode


def hash_password(
        password: str
) -> bytes:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)


def validate_password(
        password: str,
        hashed_password: bytes,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password,
    )
