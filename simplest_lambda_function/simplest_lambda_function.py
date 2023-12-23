import boto3
import json


def lambda_handler(event, context):
    '''
    '''
    print("Received event: " + json.dumps(event, indent=2))

    # This just shows how to get the HTTP method.
    operation = event['httpMethod']

    if operation in ["GET", "PUT", "DELETE"]:
        status_code = '200'
    elif operation == 'POST':
        status_code = '201'
    else:
        status_code = "501"

    # PUT, POST and DELETE are not supposed to return bodies but this lambda function
    # returns a body for debugging and demo purposes.
    body = json.dumps(event, indent=2, default=str)

    response = {
        'statuscode': status_code,
        'body': body,
        'headers': {
            'Content-Type': 'application/json'
        }
    }

    return response


