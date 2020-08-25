import hashlib
from config import token_secret
import time
import jwt
from jwt import exceptions


def hash256(data):
    sha256 = hashlib.sha256()
    sha256.update(data.encode())
    result = sha256.hexdigest()
    return result


def create_token(payload):
    headers = {"alg": "HS256", "typ": "JWT"}
    payload.update({"expire": int(time.time() + 60 * 60 * 6)})
    token = jwt.encode(
        payload=payload, key=token_secret, algorithm="HS256", headers=headers
    ).decode("utf-8")
    return token


def validate_token(token):
    payload = None
    message = None
    try:
        payload = jwt.decode(token, token_secret, True, algorithm="HS256")
    except exceptions.ExpiredSignatureError:
        message = "Token Expired"
    except jwt.DecodeError:
        message = "Token Decode Error"
    except jwt.InvalidTokenError:
        message = "Invalid Token"
    return (payload, message)
