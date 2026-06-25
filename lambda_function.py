import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('visitor-counter')

def lambda_handler(event, context):
    # Increment the visitor count
    response = table.update_item(
        Key={'id': 'visitors'},
        UpdateExpression='SET #count = #count + :val',
        ExpressionAttributeNames={'#count': 'count'},
        ExpressionAttributeValues={':val': 1},
        ReturnValues='UPDATED_NEW'
    )
    
    # Get the updated count
    count = int(response['Attributes']['count'])
    
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Content-Type': 'application/json'
        },
        'body': json.dumps({'count': count})
    }