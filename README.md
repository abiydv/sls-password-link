# Serverless: Self-service : Reset password and retrieve it using one time link 

![servrless](https://github.com/abiydv/ref-docs/blob/master/images/logos/serverless_small.png)
![py](https://github.com/abiydv/ref-docs/blob/master/images/logos/python_small.png)
![cli](https://github.com/abiydv/ref-docs/blob/master/images/logos/aws-cli_small.png)
![aws-lambda](https://github.com/abiydv/ref-docs/blob/master/images/logos/aws-lambda_small.png)

## BACKGROUND

As often needed, users have to reset their password for different systems. Sending these passwords over email is not secure. I wrote this small utility which resets a user password and saves it in the AWS Parameter store and also provides a link to extract this password ONCE. As soon as the user extracts this password - it is no longer possible to retreive it again. Once setup and running, it does not need any intervention.

An example use case could be to allow IAM users to reset their passwords if they forget it rather than requesting someone else (admin team, maybe?) to do it for them.

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

## USAGE
#### 1. Deploy the service 
Deploy the service. Use `--stage=qa|prod` to deploy the service in stages other than `dev`.
```
sls deploy -v
```
#### 2. Generate the password - 
```
curl https://apiendpoint.region.amazonaws.com/dev/generate?user=username
```
This will give you an output like - 
```
{
	message: "Password generated. Please visit the url to retrieve your password",
	link: "https://apiendpoint.region.amazonaws.com/dev/extract?p1=username&tkn=hzMWfz4oaS8Yajm43krg"
}
```
#### 3. Extract the password - 
```
curl https://apiendpoint.region.amazonaws.com/dev/extract?p1=username&tkn=hzMWfz4oaS8Yajm43krg
```
This will give you an output like - 
```
{
	message: "Notedown your initial-signon password, this link will expire after you close this page",
	password: "gLwr7np$34dW"
}
```
If you hit the same url again, it should now give you an error - 
```
{
    "message": "Link expired or used already!"
}
```

#### 4. Cleanup
:rocket: Nuke the setup after you are done testing/looking.
```
sls remove -v
```

## CONTACT

Drop me a note or open an issue if something doesn't work out.

Cheers! :thumbsup:
