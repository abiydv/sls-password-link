import json
import boto3

def extract(ph,rs,ssmclient):
    ssmclient = boto3.client('ssm')
    ssmname = "/active/{placeholder}/{randomstring}".format(
                placeholder=ph,randomstring=rs)
    expiredname = "/expired/{placeholder}/{randomstring}".format(
                placeholder=ph,randomstring=rs)

    response = ssmclient.get_parameter(Name=ssmname,WithDecryption=True)
    password = response['Parameter']['Value']
    htmlresponse = """
            <h3>Your temporary password</h3>
            <p>Please use this to login and change your password</p>
            <br>
            {password}
            """.format(password=password)
    try:
        delresponse = ssmclient.delete_parameter(Name=ssmname)
        adresponse = ssmclient.put_parameter(Name=expiredname,
            Value=password,Type='SecureString')
    except Exception as err:
        print (err)
    return htmlresponse

def begin(event, context):
    try:    
        ph = event['queryStringParameters']['ph']
        rs = event['queryStringParameters']['rs']
        ssm = boto3.client('ssm')
        htmlresponse = extract(ph,rs,ssm)
    except ssm.exceptions.ParameterNotFound:
        htmlresponse = """
            <h3>Invalid!</h3>
            <p>This link is expired or has been already used once</p>
            """
    except Exception as err:
        print(err)
        htmlresponse = """
        <h3>Internal Error</h3>
        <p>Something went wrong, please try again later.</p>
        """
    response = {
      "headers" : {"Content-Type": "text/html"},
      "statusCode" : 200,
      "body" : htmlresponse
    }

    return response
