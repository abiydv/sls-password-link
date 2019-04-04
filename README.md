# Serverless: Self-service : Reset password and retrieve it using one time link 

![servrless](https://github.com/abiydv/ref-docs/blob/master/images/logos/serverless_small.png)
![py](https://github.com/abiydv/ref-docs/blob/master/images/logos/python_small.png)
![cli](https://github.com/abiydv/ref-docs/blob/master/images/logos/aws-cli_small.png)
![aws-lambda](https://github.com/abiydv/ref-docs/blob/master/images/logos/aws-lambda_small.png)
![aws-apigateway](https://github.com/abiydv/ref-docs/blob/master/images/logos/aws-apig_small.png)
![aws-ses](https://github.com/abiydv/ref-docs/blob/master/images/logos/aws-ses_small.png)
![aws-ssm](https://github.com/abiydv/ref-docs/blob/master/images/logos/aws-ssm_small.png)

## BACKGROUND
As often happens, users have to reset their password for different systems. Sending these passwords over email is not secure. I wrote this small utility which resets a user password and saves it in the AWS Parameter store and also emails a dynamically generated link to user to extract the password. As soon as the user extracts this password - it is no longer possible to retreive it again. The link stops working. Once setup and running, it does not need any manual intervention from admin teams.

An example use case is to allow IAM users to reset their passwords if they forget it rather than requesting someone else (admin team, maybe?) to do it.

Needless to say, this is NOT a full blown solution as you will need to take care of authentication and authorization of the api (currently it is public). Treat this more as a proof of concept to use/implement using native AWS services without adopting any additional tools.

## ARCHITECTURE
This is a simplified view of the components being used. It is fairly lightweight and as part of a bigger setup, it probably wouldn't even be noticed w.r.t cost.
![arch](https://github.com/abiydv/ref-docs/blob/master/images/arch/GH_PWD_LINK.png)

## BEFORE YOU BEGIN
#### 1. Serverless. 
Install serverless, follow this [guide](https://serverless.com/framework/docs/providers/aws/guide/installation/)
  
#### 2. AWS Cli
Setup aws cli with profiles matching environments/stages. A sample `~/.aws/credentials` file - 
```
[dev]
aws_access_key_id = DEV_ACCESS_KEY
aws_secret_access_key = DEV_SECRET_KEY
```

## PREREQUISITES/ASSUMPTIONS 
You can obviously tweak the solution to work for you, but for it to work right out of the box, following should be available
 - IAM user should exist.
 - IAM username should be the user's email.
 - You should be out of SES sandbox mode, otherwise users will not receive email with the link.

## USAGE
#### 1. Deploy the service 
Deploy the service. Use `--stage=qa|prod` to deploy the service in stages other than `dev`.
```
sls deploy -v
```

#### 2. Generate the password
Hit the apigateway endpoint url `https://apiendpoint.execute-api.region.amazonaws.com/dev/generate?user=username` with the query string `user=username` to generate the password. This will give you an output like this - 
```
Your request has been submitted

Please check your email for further details
```

A sample email
```
From: no-reply@example.com
Sent: Monday, April 01, 2000 1:00 PM
To: username@example.com
Subject: CONFIDENTIAL: Account information

You can retrieve your password from the link below. 

https://apiendpoint.execute-api.region.amazonaws.com/dev/extract?ph=2000040113001245&rs=i093tN.3UOIW1YZsMi 

NOTE: This link is valid for a single use only. 
```

#### 3. Extract the password
Using the link mentioned in the email `https://apiendpoint.execute-api.region.amazonaws.com/dev/extract?ph=2000040113001245&rs=i093tN.3UOIW1YZsMi `, you can extract the password. This will give you an output like - 
```
Your temporary password

Please use this to login and change your password

ABCD_&abcd99 
```

If you hit the same url again, it should now give you an error - 
```
Invalid!

This link is expired or has been already used once
```

#### 4. Cleanup
:rocket: Nuke the setup after you are done testing/looking.
```
sls remove -v
```

## SECURITY 
Since this is a mere proof-of-concept solution, before deploying it to a live environment, you should consider implementing security measures like (listing a few, there may be more) -
 - Authentication and authorization of the api, maybe using AWS Cognito.
 - Restricting the api to within your corporate network using WAF IP based rules.
 - Restricting lambda role IAM permissions to least possible, removing any * in the policy.
 - Using a custom KMS key for encryption and tightly controlling access to this key using IAM policies.
 
## CONTACT
Drop me a note or open an issue if something doesn't work out.

Cheers! :thumbsup:
