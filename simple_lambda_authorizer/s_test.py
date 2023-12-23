import json
import simplest_lambda_authorizer as s_auth


def load_event(event_name=None):

    if event_name is None:
        event_name = "event_1"

    result = None
    with open("test_event.json") as in_file:
        result = json.load(in_file)
        result = result.get(event_name)

    return result


def t1(event_name=None):
    e = load_event(event_name)
    r = s_auth.lambda_handler(e, None)
    print("t1 result = \n", json.dumps(r, indent=2))


def t2():
    s = s_auth.get_secret()
    print("Secret = ", s)


def t3():
    sec = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyLCJwZXJtaXNzaW9ucyI6W3siYXBpIjoibjNwdW5tanBnNCIsInN0YWdlIjoiZGVmYXVsdCIsIm1ldGhvZCI6IkdFVCIsInJlc291cmNlIjoic2ltcGxlc3RfbGFtYmRhIn1dfQ.Qtyygf1fmlyvFg_aF_SNYahNBzvDTT5CYmq9L-BHGs0"
    res = s_auth.decode_scope(sec)
    print("t3: result = \n", res)


if __name__ == "__main__":
    t1()
    # t2()
    # t3()


