
[DEPRECATED!!!] Twilio SMS Capture (using AWS Gateway) 
======================================================

**REPOSITORY DEPRECATED!!! See section 4.1!!**

## Problem

- Mobile apps build using AWS Mobile Services often require SMS OTP to log in into existing account from a new device
- For mobile app Testflight Apple approval, you often need to provide existing account credentials, so that the Apple reviewer can log in into the app 

## Solutions

There are a few solutions to this problem: 

### 1. A horrible one 

Turn off 2FA on the test account. Sounds easy, but is difficult in practice: you want to have a mandatory 2FA turned on on AWS production user pool for security reasons. If that's the case, you can't switch it off for just one account. 

### 2. A not-so-good one

Have MFA optional on your user pool, but switch it on in AWS Lambda on account creation. Then manually switch it off for the test account. 

This approach is better, but it makes it optional to have 2FA on your whole production user pool, which is not ideal. 

### 3. An OK-ish but difficult one

Implement your SMS OTP verification manually and return a same static code for a test account. 

By default AWS Cognito provides an OTP phone verification implementation that works out of the box. If you want to customise it to return a static code for a specific account, I believe you need to implement custom Cognito authentication flows and generate OTPs manually. This is a significant effort, but is doable. One way to do that would be to use Twilio account to generate OTP passwords. 

I have not explored this method in practice as it seemed to require a bit too much effort. It also requires taking control of the OTP generation process for all users, which requires maintenance (as opposed to an automatic solution provided by Cognito out of the box). 

[Discussion on Stack Overflow](https://stackoverflow.com/questions/45453416/apple-rejects-app-because-test-account-not-given-as-app-login-via-otp-only)

### 4. An OK solution this tutorial focuses on

Register your production test account for Testflight with a phone number managed by Twilio. Create a service/webpage that displays the last message received by that number. Pass the address of that service to Apple reviewer. 

This is not difficult and has been proven to work with Apple review process. It also doesn't require changing your production AWS User Pool configuration or your OTP generation process. 

[Discussion on Apple forums](https://developer.apple.com/forums/thread/125961)

#### 4.1. UPDATE: 
**This didn't actually work! AWS refuses to send the OTP code to a Twilio-managed phone numer!!
The solution still allows to expose last SMS from a Twilio-managed number under an API Gateway, but is not fig for purpose (you can't read AWS OTPs, since they don't get send by AWS Cognito. I've not tested with a custom SMS sender lambda, not sure if that'd work). 
The solution we ended up implementing was to let users whitelisted as apple reviewer accounts sign in without returning an OTP (using a custom login lambda).**

## Solution overview

1. Create a Twilio phone number 
2. Create an AWS Lambda function that takes in the SMS message incoming from Twilio, parses it and stores the value in DynamoDB
3. Create an AWS API Gateway for that lambda: a POST Rest API endpoint 
4. Configure the endpoint to receive incoming data as XML (from Twilio) and convert it to JSON
5. Return an XML response for Twilio from the lambda 
6. Create a DynamoDB table for that lambda to write the captured text message to 
7. Setup the API Gateway POST endpoint as an incoming message Webhook on Twilio 
8. Write a new AWS Lambda that reads the value from DynamoDB, wraps it in a JSON and returns it 
9. Put that new Lambda behind a GET endpoint of the API Gateway 

At the end of this process you should have a publicly available endpoint that you can hit in your browser and you'll see the last text message received by the connected virtual phone number.


## Detailed instructions

It should take less than an hour to follow the instructions below and get up and running. 

1. Follow the tutorial below for a basic AWS lambda and API Gateway setup for a Twilio account:

[A detailed tutorial on how to reply to messages in Python with AWS Lambda](https://www.twilio.com/docs/sms/tutorials/how-to-receive-and-reply-python-amazon-lambda)

2. Use the code from `reply_messages_lambda.py` in this repository for the POST endpoint. 

3. Manually create a table `TwilioMessages` in DynamoDB.

4. Create a GET API gateway (with default configuration) using `get_last_code_lambda.py`. Make sure the authentication on that API Gateway is set to 'None', so that it's accessible online. 

5. Deploy the API. Send a text message to the Twilio account number and go to the API Gateway GET endpoint URL in your browser. Verify that the text message you just send was returned.

6. If the Get API endpoint does not display the code, use AWS CloudWatch to see the lambda error and debug the problem. 
