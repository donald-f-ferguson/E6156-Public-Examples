import jwt
from pydantic import BaseModel
from typing import List


class SecurityScope(BaseModel):
    email: str
    allowed_urls: List[str]


class SecurityEngine:

    default_secret = "this is not a secret"

    def __init__(self, key=None, algorithms=None):
        if key is None:
            self.secret_key = SecurityEngine.default_secret
        else:
            self.secret_key = key

        if algorithms is None:
            self.algorithms = "HS256"
        else:
            self.algorithms = algorithms

    def decode_token(self, token):

        try:
            result = jwt.decode(jwt=token,
                                key=self.secret_key,
                                algorithms=self.algorithms
                                )
        except Exception as e:
            print("Decode failed")
            result = None

        return result

    def encode_token(self, token_data):

        try:
            result = jwt.encode(payload=token_data,
                                key=self.secret_key,
                                algorithm=self.algorithms
                                )
        except Exception as e:
            print("Decode failed")
            result = None

        return result

    def check_scope(self, path, auth_token):

        scope = self.decode_token(auth_token)
        