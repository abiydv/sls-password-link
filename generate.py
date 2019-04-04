import re
import os
import boto3
import secrets
import datetime

def generaterandomnumbers():
    now = datetime.datetime.now()
    numbers = now.strftime('%Y%m%d%H%M%S') + ('%02d' % (now.microsecond / 10000))
    return numbers

def randomuppercase(chars):
    charset="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    randomstring = "".join([secrets.choice(charset) for _ in range(0, chars)])
    return randomstring

def randomlowercase(chars):
    charset="abcdefghijklmnopqrstuvwxyz"
    randomstring = "".join([secrets.choice(charset) for _ in range(0, chars)])
    return randomstring

def randomspecialchar(chars):
    charset="_=#!$&"
    randomstring = "".join([secrets.choice(charset) for _ in range(0, chars)])
    return randomstring

def randomnumbers(chars):
    charset="0123456789"
    randomstring = "".join([secrets.choice(charset) for _ in range(0, chars)])
    return randomstring

def generaterandomstring(chars):
    charset="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.-_"
    randomstring = "".join([secrets.choice(charset) for _ in range(0, chars)])
    return randomstring

def generatepassword(user):
    iamclient = boto3.client('iam')
    ssmclient = boto3.client('ssm')
    userpassword = randomuppercase(4) + randomspecialchar(2) + randomlowercase(4) + str(randomnumbers(2))
    randomstring = generaterandomstring(18)
    placeholder = generaterandomnumbers()
    print(userpassword)
    response = iamclient.update_login_profile(
        UserName=user,Password=userpassword,PasswordResetRequired=True)

    ssmname = "/active/{placeholder}/{randomstring}".format(
                placeholder=placeholder,randomstring=randomstring)

    response = ssmclient.put_parameter(
        Name=ssmname,Value=userpassword,Type='SecureString')

    domain = os.environ['serviceapi']
    pwdurl = "{domain}/extract?ph={placeholder}&rs={randomstring}".format(
        domain=domain,placeholder=placeholder,randomstring=randomstring)
    return pwdurl

def validate(username):
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@example.com$', username)
    if match is None:
        raise ValueError("Invalid",username)
    else:
        print ("Valid " + username)
    return "VALID"

def notify(user,link):
    mailfrom = "no-reply@example.com"
    subject = "CONFIDENTIAL: Account information"
    message = """
    You can retrieve your password from the link below.
    <br><br>
    {link}
    <br><br>
    NOTE: This link is valid for a single use only.
    """.format(link=link)

    ses = boto3.client('ses')
    response = ses.send_email(
        Source=mailfrom,Destination={'ToAddresses': [ user ]},
        Message={'Subject': {'Data': subject,'Charset': 'utf8'},
            'Body': {'Html': {'Data': message,'Charset': 'utf8'}}})
    return "SUCCESS"

def begin(event, context):
    try:
        user = event['queryStringParameters']['user']
        validate(user)
        pwdurl = generatepassword(user)
        notify(user,pwdurl)
        htmlresponse = """
            <h3>Your request has been submitted</h3>
            <p>Please check your email for further details</p>
            """
    except ValueError as verr:
        print("Error: Invalid user specified, must be of the form xyz@example.com")
        htmlresponse = """
            <h3>Your request could not be submitted</h3>
            <p>Please contact the AWS team</p>
            """
        
    response = {
          "headers" : {"Content-Type": "text/html"},
          "statusCode" : 200,
          "body" : htmlresponse
    }
    return response
