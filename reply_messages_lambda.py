import boto3
import json

def put_value_in_dynamo_db(text):
    dynamodb = boto3.resource('dynamodb')
    event = {
        'id': 1,
        'body': text
    }

    table = dynamodb.Table('TwilioMessages')

    # Naive implementation: deleting and item and putting a new one
    # instead of updating existing one. Feel free to fix it.

    table.delete_item(
        Key={
            'id': 1,
        },
    )
    table.put_item(Item=event)

def lambda_handler(event, context):
    print('Received event: ' + str(event))

    # Body tag is capitalised in Twilio, but lowercase in AWS sample event template, watch out for that
    body = event['Body']

    print('Event body: ' + body)
    put_value_in_dynamo_db(body)

    return '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'\
           '<Response><Message><Body>Hello world! -Lambda</Body><Media>https://demo.twilio.com/owl.png</Media></Message></Response>'
