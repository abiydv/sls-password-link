import os
import json
import boto3
import secrets

def generaterandomstring(chars):
    charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@$&"
    return("".join([secrets.choice(charset) for _ in range(0, chars)]))

def begin(event, context):
    user = event['queryStringParameters']['user']
    password = generaterandomstring(12)
    randomstring = generaterandomstring(20)
    name='/pwdservice/{user}/{randomstring}'.format(user=user,randomstring=randomstring)
    print(name)
    client = boto3.client('ssm')
    response = client.put_parameter(Name=name,Value=password,Type='SecureString',Overwrite=False)
    link = os.environ['serviceapi'] + "/extract?p1={p1}&tkn={tkn}".format(p1=user,tkn=randomstring)
    body = {
        "message": "Password generated. Please visit the url to retrieve your password",
        "link": link
    }
    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response