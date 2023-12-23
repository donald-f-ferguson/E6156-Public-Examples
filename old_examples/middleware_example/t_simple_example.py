import requests


def t1():

    url = "http://localhost:8002/another"

    print("t1: Testing without API Key.")
    res = requests.get(url)
    print("t1: Status code = ", res.status_code)

    if res.status_code == 200:
        print("t1: Status code 200 should not have happened.")
    elif res.status_code == 401:
        print("t1: Status code 401 is the correct answer.")
    else:
        print("t1: Huh?")


if __name__ == "__main__":
    t1()




