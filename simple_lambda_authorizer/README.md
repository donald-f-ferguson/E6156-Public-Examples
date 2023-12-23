# Simplest Lambda Function

## Overview

This is a simple API GW Lambda authorizer. This __is not__ a JWT authorizer,
which is much different. The code is from the default template produced
by selecting the authorizer blueprint when creating the lambda function.

The authorizer is configured on the GW and configured to receive the ```entire
request``` for its input event. This is in contrast to the configuration in which
the authorizer on receives the token and mathodArn.

The authorizer is configured to return a policy document.

The input and return formats are configurable when attaching the policy
the authorizer to the resource and method.

## Behavior

In my example, the authorizer looks for a simple Bearer Token in the
```Authorization``` header.
    - https://oauth.net/2/bearer-tokens/
    - The token format is a JWT document.

The JWT document is of the form:
```
{
  "sub": "1234567890",
  "name": "John Doe",
  "iat": 1516239022,
  "permissions": [
    {
      "api": "n3punmjpg4",
      "stage": "default",
      "method": "GET",
      "resource": "simplest_lambda"
    }
  ]
}
```
```sub``` and ```iat``` are standard claims.
https://auth0.com/docs/secure/tokens/json-web-tokens/json-web-token-claims

```permissions``` is an array of authorization rules specifying what the 
subject is allowed to do. 
- ```api``` is the AWS API GW API ID
- ```stage``` is the stage
- ```method``` is the allowed HTTP method.
- ```resource``` is the GW resource.

This is a simplistic format just for example purposes.

The authorizer returns an simplistic AWS policy document
(https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html)

A simple example is:

```
{
  "principalId": "1234567890",
  "policyDocument": {
    "Version": "2012-10-17",
    "Statement": [
      {
        "Action": "execute-api:Invoke",
        "Effect": "Allow",
        "Resource": [
          "arn:aws:execute-api:us-east-1:150198544176:n3punmjpg4/default/*/*"
        ]
      }
    ]
  },
  "context": {
    "key": "value",
    "number": 1,
    "bool": true
  }
}
```


## Example Structure

- The directories ```jwt``` and ```PyJWT-2.8.0.dist-info``` are python JWT packages.
The authorizer uses pyJWT to decode the signed token. Instead of setting up
Lambda Function layers, I pip install locally and put into the deployment zip file.
    - https://docs.aws.amazon.com/lambda/latest/dg/chapter-layers.html
    - https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-package.html

- ```lambda.zip``` is the deployment zip file.
- ```s_test``` is  simple set of local tests. For the tests to run, the requirements are:
  - AWS credentials configured.
  - Configured credentials have permission to retrieve secret from AWS Secrets Manager.

- ```simplest_lambda_authorizer.py``` is the authorizer.

- ```test_event.json``` is a test API GW event coming into the lambda, which will be
passed to the authorizer.


- ```new_simple_lambda_authorizer.yaml``` is a generated SAM
  (https://aws.amazon.com/serverless/sam/) file downloaded to describe the deployed authorizer.

- ```simplest_api-default-oas30-apigateway.yaml``` is the exported API definition.
I manually configured the API GW and exported the definition.


## Notes and Hints

- The API GW for this example simply invokes the Lambda function in the
```simplest_lambda_function.```

- To help professor Ferguson find the deployed example in his morass of AWS stuff.
  - Authorizer lambda function name: ```new_simple_lambda_authorizer```
  - API GW: ```simplest_api```

- For debugging, make sure the Lambda Authorizer has permission to write to CloudWatch.

- The deployed authorization must have permission to read secrets.

- I created a ```REST API``` configuration for the GW.

- When testing, if you do not set an authorization header, the lambda authorizer
will not log to CloudWatch.

## Deployment

For this simple example, I just copy the code into the code window on AWS.