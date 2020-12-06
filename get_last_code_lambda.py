import boto3
import json

def read_code_from_dynamodb():
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('TwilioMessages')

    query = table.get_item(
            Key={
                'id': 1,
            }
        )

    if 'Item' in query:
        body = query['Item']['body']
        print(body)
        return '{ "code": "' + body + '"}'

def lambda_handler(event, context):
    return read_code_from_dynamodb()
