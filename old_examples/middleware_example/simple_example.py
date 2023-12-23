#
# This example is copied from and evolved from
# https://medium.com/@saverio3107/mastering-middleware-in-fastapi-from-basic-implementation-to-route-based-strategies-d62eff6b5463
#
#
from fastapi import FastAPI, Request, Response, HTTPException
from datetime import datetime
import uvicorn


app = FastAPI()

API_KEY = "my_secret_api_key"


# First Middleware: Logging request details
@app.middleware("http")
async def log_request_details(request: Request, call_next):
    method_name = request.method
    path = request.url.path
    with open("request_log.txt", mode="a") as reqfile:
        content = f"Method: {method_name}, Path: {path}, Received at: {datetime.now()}\n"
        reqfile.write(content)

    response = await call_next(request)

    with open("response_log.txt", mode="a") as reqfile:
        t = str(response)
        content = f"Method: {method_name}, Path: {path}, Response: {t}\n"
        reqfile.write(content)

    return response


# Second Middleware: API key authentication
@app.middleware("http")
async def api_key_authentication(request: Request, call_next):
    api_key = request.headers.get("X-Api-Key")
    if api_key != API_KEY:
        # The original code is wrong. There is an issue with raise HTTPException
        # inside middleware.
        fail_response = Response(status_code=401, content="Not Authenticated.")
    else:
        fail_response = None

    response = await call_next(request)

    if fail_response:
        response = fail_response

    return response




@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


@app.get("/another")
async def read_another():
    return {"message": "This is another endpoint"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8002)