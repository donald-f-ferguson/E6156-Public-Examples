import requests

auth_header = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.rqmqjmeRgLlbvXJW_sbyc1bhl4hiINhVSFkCKeKttkA"

result = request.get(
    url="https://zt5yh6abm7.execute-api.us-east-1.amazonaws.com/default/simple-lambda-echo",
    headers = {
        "Authorization": auth_header
    }
)