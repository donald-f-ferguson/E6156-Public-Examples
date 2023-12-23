"""
This is a Lambda authorizer for the AWS API Gateway. The basic code comes from
selecting the Lambda Authorizer template when creating a Lambda function through
the console. I have modified the example to show some concepts.
"""
import re
import json
import jwt
import boto3
from botocore.exceptions import ClientError


def get_secret():
    """
    Retrieve the encryption/signing secret from the AWS Secrets Manager.
    https://aws.amazon.com/secrets-manager/

    :return: The secret key for checking signatures of authorization tokens.
    """

    # These should be environment variables following best practice guidelines.
    # https://12factor.net/config
    #
    # Since this is an example, I just put the constants in the code.
    #
    secret_name = "Simplest_Authorizer_Secret"
    secret_label = "e6156_secret"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/secretsmanager/client/get_secret_value.html
    # for the format of the response. I saved the secret as a string.
    #
    secret = get_secret_value_response['SecretString']

    # The secret string is a name/value (JSON) object serialized into a string.
    # Load the string into a dictionary
    #
    result = json.loads(secret)

    # Get the specific secret I want.
    result = result.get(secret_label, None)

    return result


def decode_scope(scope):
    """
    The scope is authorization information encoded in an array in a JWT token.
    #
    :param scope: The scope/authorization token.
    :return:
    """
    secret = get_secret()
    decoded_scope = jwt.decode(scope, secret, algorithms=["HS256"])
    return decoded_scope


def valid_scope(auth_info, api, stage, method, resource):
    """

    The format of the authorization token is:

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
            },
            {
                ... ...
            }
        ]
    }

    This is not a standard format. It is just simple for example purposes.

    Each authorization rule is a dictionary of the form:
        - api is the API ID from the AWS API Gateway.
        - stage is the API deployed stage
        - method is an HTTP verb
        - resource is a resource defined in the API definition


    :param auth_info: The encoded authorization token.
    :param api: The API ID in the incoming request.
    :param stage: The stage in the incoming request.
    :param method: The HTTP method in the incoming request.
    :param resource: The resource in the incoming request.
    :return: True or False based on whether or not the token contains an access authorization for the
        method on the resource.
    """
    try:
        # Retrieve the list of authorization rules.
        #
        scope = auth_info["scope"]

        # Iterate through the authorization rules in the scope to determine
        # if the Authorization token containers permission for the operation.
        #
        for s in scope:
            if s["api"] == api and \
                    s["method"] == method and \
                    s["stage"] == stage and \
                    s["resource"] == resource:
                valid = True
                break
        else:
            valid = False
    except Exception as e:
        print("Exception = ", e)
        valid = False

    return valid


def lambda_handler(event, context):
    """
    There are two basic formats that you can figure for input into the authorizer.
        1. The authorizer can receive the entire incoming event from the gateway.
        2. The authorizer receives only the Authorization token from the header and the method ARN,

    There are two return formats for a Lambda Authorizer:
        1. A simple True or False authorization decision.
        2. An AWS policy document containing permissions for this request. This is the format that
            this method returns. But, it is a very simple format/example.

    :param event: The input event to the Lambda function.
    :param context: The input context.
    :return: The policy document.
    """

    print("Event = ", json.dumps(event))

    # The default decision is to deny access.
    result = "Deny"

    '''
    We look for a JWT Authorization header.
    '''
    try:
        """
        See the AWS documentation for the format of an API Gateway event into a Lambda function.
        """

        # In my example, the format of the token is "Bearer sdkljfsdjf;lsdjfl;s..."
        # This is a simple bearer token.
        #
        auth_token = event["headers"]["Authorization"]

        # Get an array of the form ["Bearer", "sdkljfsdjf;lsdjfl;s..."]
        # and extract the encoded value.
        #
        auth_info = auth_token.split(" ")
        if auth_info[0] == "Bearer":
            auth_info = decode_scope(auth_info[1])
        else:
            raise ValueError("Not a bearer token.")

        # In JWT, the "sub" is the ID of the user/identity that requested the token.
        principalId = auth_info["sub"]

    except Exception as e:
        print("Exception e = ", e)
        raise Exception('Unauthorized')

    '''
    Read the information in the comments of the sample authorizer created by the template
    when creating a Lambda authorizer through the AWS Console. The yemplate provides the
    base code, which I have modified.
    '''

    # The method ARN in the incoming event is something like ... ...
    # "arn:aws:execute-api:us-east-1:150198544176:n3punmjpg4/default/GET/simplest_lambda"
    # This code segment split the ARN, gets the path of the form /apiId/stage/method/resource,
    # and then splits the path to get the elements.
    #
    tmp = event['methodArn'].split(':')
    apiGatewayArnTmp = tmp[5].split('/')
    api = apiGatewayArnTmp[0]
    stage = apiGatewayArnTmp[1]
    method = apiGatewayArnTmp[2]
    resource = apiGatewayArnTmp[3]

    awsAccountId = tmp[4]

    # Generate the default policy document. See the AuthPolicy class below, which comes directly
    # from the AWS Examples.
    #
    policy = AuthPolicy(principalId, awsAccountId)
    policy.restApiId = apiGatewayArnTmp[0]
    policy.region = tmp[3]
    policy.stage = apiGatewayArnTmp[1]

    # If the scope contains a rule authorizing the operation, set the policy to allow all methods.
    # This is lazy and I should only authorize the requested method.
    #
    if valid_scope(auth_info, api, stage, method, resource):
        policy.allowAllMethods()
    else:
        policy.denyAllMethods()

    # Finally, build the policy
    authResponse = policy.build()

    # The follow code comes from tne AWS example.
    #
    # new! -- add additional key-value pairs associated with the authenticated principal
    # these are made available by APIGW like so: $context.authorizer.<key>
    # additional context is cached
    context = {
        'key': 'value',  # $context.authorizer.key -> value
        'number': 1,
        'bool': True
    }
    # context['arr'] = ['foo'] <- this is invalid, APIGW will not accept it
    # context['obj'] = {'foo':'bar'} <- also invalid

    # Include the context in the response.
    authResponse['context'] = context

    print("Response = ", authResponse)

    return authResponse


# *****************************************************************************************************************
#
# All of the code below comes directly from the example provided by AWS.
#
# There is a lot of complexity and sophistication in the created policy document that is
# not necessary to understand the example.
#

class HttpVerb:
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    PATCH = 'PATCH'
    HEAD = 'HEAD'
    DELETE = 'DELETE'
    OPTIONS = 'OPTIONS'
    ALL = '*'


class AuthPolicy(object):
    # The AWS account id the policy will be generated for. This is used to create the method ARNs.
    awsAccountId = ''
    # The principal used for the policy, this should be a unique identifier for the end user.
    principalId = ''
    # The policy version used for the evaluation. This should always be '2012-10-17'
    version = '2012-10-17'
    # The regular expression used to validate resource paths for the policy
    pathRegex = '^[/.a-zA-Z0-9-\*]+$'

    '''Internal lists of allowed and denied methods.

    These are lists of objects and each object has 2 properties: A resource
    ARN and a nullable conditions statement. The build method processes these
    lists and generates the approriate statements for the final policy.
    '''
    allowMethods = []
    denyMethods = []

    """Replace the placeholder value with a default API Gateway API id to be used in the policy.
    Beware of using '*' since it will not simply mean any API Gateway API id, because stars will greedily expand over '/' or other separators.
    See https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_resource.html for more details."""
    restApiId = "m2xztv82q6"

    """Replace the placeholder value with a default region to be used in the policy.
    Beware of using '*' since it will not simply mean any region, because stars will greedily expand over '/' or other separators.
    See https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_resource.html for more details."""
    region = "us-east-1"

    """Replace the placeholder value with a default stage to be used in the policy.
    Beware of using '*' since it will not simply mean any stage, because stars will greedily expand over '/' or other separators.
    See https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_resource.html for more details."""
    stage = "default"

    def __init__(self, principal, awsAccountId):
        self.awsAccountId = awsAccountId
        self.principalId = principal
        self.allowMethods = []
        self.denyMethods = []

    def _addMethod(self, effect, verb, resource, conditions):
        '''Adds a method to the internal lists of allowed or denied methods. Each object in
        the internal list contains a resource ARN and a condition statement. The condition
        statement can be null.'''
        if verb != '*' and not hasattr(HttpVerb, verb):
            raise NameError('Invalid HTTP verb ' + verb + '. Allowed verbs in HttpVerb class')
        resourcePattern = re.compile(self.pathRegex)
        if not resourcePattern.match(resource):
            raise NameError('Invalid resource path: ' + resource + '. Path should match ' + self.pathRegex)

        if resource[:1] == '/':
            resource = resource[1:]

        resourceArn = 'arn:aws:execute-api:{}:{}:{}/{}/{}/{}'.format(self.region, self.awsAccountId, self.restApiId,
                                                                     self.stage, verb, resource)

        if effect.lower() == 'allow':
            self.allowMethods.append({
                'resourceArn': resourceArn,
                'conditions': conditions
            })
        elif effect.lower() == 'deny':
            self.denyMethods.append({
                'resourceArn': resourceArn,
                'conditions': conditions
            })

    def _getEmptyStatement(self, effect):
        '''Returns an empty statement object prepopulated with the correct action and the
        desired effect.'''
        statement = {
            'Action': 'execute-api:Invoke',
            'Effect': effect[:1].upper() + effect[1:].lower(),
            'Resource': []
        }

        return statement

    def _getStatementForEffect(self, effect, methods):
        '''This function loops over an array of objects containing a resourceArn and
        conditions statement and generates the array of statements for the policy.'''
        statements = []

        if len(methods) > 0:
            statement = self._getEmptyStatement(effect)

            for curMethod in methods:
                if curMethod['conditions'] is None or len(curMethod['conditions']) == 0:
                    statement['Resource'].append(curMethod['resourceArn'])
                else:
                    conditionalStatement = self._getEmptyStatement(effect)
                    conditionalStatement['Resource'].append(curMethod['resourceArn'])
                    conditionalStatement['Condition'] = curMethod['conditions']
                    statements.append(conditionalStatement)

            if statement['Resource']:
                statements.append(statement)

        return statements

    def allowAllMethods(self):
        '''Adds a '*' allow to the policy to authorize access to all methods of an API'''
        self._addMethod('Allow', HttpVerb.ALL, '*', [])

    def denyAllMethods(self):
        '''Adds a '*' allow to the policy to deny access to all methods of an API'''
        self._addMethod('Deny', HttpVerb.ALL, '*', [])

    def allowMethod(self, verb, resource):
        '''Adds an API Gateway method (Http verb + Resource path) to the list of allowed
        methods for the policy'''
        self._addMethod('Allow', verb, resource, [])

    def denyMethod(self, verb, resource):
        '''Adds an API Gateway method (Http verb + Resource path) to the list of denied
        methods for the policy'''
        self._addMethod('Deny', verb, resource, [])

    def allowMethodWithConditions(self, verb, resource, conditions):
        '''Adds an API Gateway method (Http verb + Resource path) to the list of allowed
        methods and includes a condition for the policy statement. More on AWS policy
        conditions here: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html#Condition'''
        self._addMethod('Allow', verb, resource, conditions)

    def denyMethodWithConditions(self, verb, resource, conditions):
        '''Adds an API Gateway method (Http verb + Resource path) to the list of denied
        methods and includes a condition for the policy statement. More on AWS policy
        conditions here: http://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html#Condition'''
        self._addMethod('Deny', verb, resource, conditions)

    def build(self):
        '''Generates the policy document based on the internal lists of allowed and denied
        conditions. This will generate a policy with two main statements for the effect:
        one statement for Allow and one statement for Deny.
        Methods that includes conditions will have their own statement in the policy.'''
        if ((self.allowMethods is None or len(self.allowMethods) == 0) and
                (self.denyMethods is None or len(self.denyMethods) == 0)):
            raise NameError('No statements defined for the policy')

        policy = {
            'principalId': self.principalId,
            'policyDocument': {
                'Version': self.version,
                'Statement': []
            }
        }

        policy['policyDocument']['Statement'].extend(self._getStatementForEffect('Allow', self.allowMethods))
        policy['policyDocument']['Statement'].extend(self._getStatementForEffect('Deny', self.denyMethods))

        return policy
