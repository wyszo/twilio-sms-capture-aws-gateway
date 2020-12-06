
Twilio SMS Capture
==================

Problem:
- Mobile apps build using AWS Mobile Services often require SMS OTP to log in into existing account from a new device
- For mobile app Testflight Apple approval, you often need to provide existing account credentials, so that the Apple reviewer can log in into the app 

Solutions: 

There are a few solutions to this problem: 

1. (a horrible one) Turn off 2FA on the test account. Sounds easy, but is difficult in practice: you want to have a mandatory 2FA turned on on AWS production user pool for security reasons. If that's the case, you can't switch it off for just one account. 

2. (a not-so-good one) Have MFA optional on your user pool, but switch it on in AWS Lambda on account creation. Then manually switch it off for the test account. 

This approach is better, but it makes it optional to have 2FA on your whole production user pool, which is not ideal. 

3. (an OK-ish but difficult one) Implement your SMS OTP verification manually and return a same static code for a test account. 

By default AWS Cognito provides an OTP phone verification implementation that works out of the box. If you want to customise it to return a static code for a specific account, I believe you need to implement custom cognito authentication flows and generate OTPs manually. This is a significant effort, but is doable. One way to do that would be to use Twilio account to generate OTP passwords. 

I have not explored this method in practice as it seemed to require a bit too much effort. It also requires taking control of the OTP generation process for all users, which requires maintenance (as opposed to an automatic solution provided by Cognito out of the box). 

[Discussion on Stack Overflow](https://stackoverflow.com/questions/45453416/apple-rejects-app-because-test-account-not-given-as-app-login-via-otp-only)

4. (an OK solution this tutorial focuses on) Register your production test account for Testflight with a phone number managed by Twilio. Create a service/webpage that displays the last message received by that number. Pass the address of that service to Apple reviewer. 

This is not difficult and has been proven to work with Apple review process. It also doesn't require changing your production AWS User Pool configuration or your OTP generation process. 

[Discussion on Apple forums](https://developer.apple.com/forums/thread/125961)

Solution overview
-----------------

