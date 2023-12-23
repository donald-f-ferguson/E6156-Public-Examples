import json

from old_examples.security.dff_security_engine import DFF_Security as DFF_Security


def t1():
    ds = DFF_Security()

    jwt_info = {
            "sub": "1234567890",
            "name": "John Doe",
            "cool_dude": "Of course!",
            "iat": 1516239022
    }

    token = ds.encode_token(jwt_info)
    print("t1: Encoded token = ", token)


def t2():
    ds = DFF_Security()

    # Used JWT.io to encode using secret.
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiY29vbF9kdWRlIjoiT2YgY291cnNlISIsImlhdCI6MTUxNjIzOTAyMn0.UN2wXrK7mzU_B1dZnWtHQOMA8G_sVrtMFx3XMdeapFM"
    d = ds.decode_token(token)

    print("t2 decode = \n", json.dumps(d, indent=2))


if __name__ == "__main__":
    # t1()
    t2()
