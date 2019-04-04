import json
import boto3

def begin(event, context):
    user = event['queryStringParameters']['p1']
    tkn = event['queryStringParameters']['tkn']
    
    ssm = boto3.client('ssm')
    name='/pwdservice/{user}/{tkn}'.format(user=user,tkn=tkn)
    try:
        response = ssm.get_parameter(Name=name,WithDecryption=True)
        password = response['Parameter']['Value']
        body = {
            "message": "Notedown your initial-signon password, this link will expire after you close this page",
            "password": password
        }
        dresp = ssm.delete_parameter(Name=name)
    except ssm.exceptions.ParameterNotFound:
        body = {
            "message": "Link expired or used already!"
        }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response