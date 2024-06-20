from decimal import Decimal
import json
import boto3
import os
import uuid
from botocore.exceptions import ClientError
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(
    table_name)


def lambda_handler(event, context):
    body = json.loads(event['body'])
    item_name = body['name']
    category = body['category']
    price = Decimal(str(body['price']))

    last_updated_at = datetime.now().isoformat()

    # Check if item_name exists
    response = table.query(
        IndexName='ItemNameIndex',
        KeyConditionExpression=boto3.dynamodb.conditions.Key(
            'item_name').eq(item_name)
    )
    if response['Items']:
        # Update existing item
        item_id = response['Items'][0]['id']
        try:
            table.update_item(
                Key={'id': item_id},
                UpdateExpression="set price = :p, category = :c, last_updated_at = :lud",
                ExpressionAttributeValues={
                    ':p': price,
                    ':c': category,
                    ':lud': last_updated_at,
                },
                ReturnValues="UPDATED_NEW"
            )
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                },
                'body': json.dumps({'id': item_id})
            }
        except ClientError as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                },
                'body': json.dumps(f"Error updating item: {e.response['Error']['Message']}")
            }
    else:
        # Insert new item
        item_id = str(uuid.uuid4())
        try:
            response = table.put_item(
                Item={
                    'id': item_id,
                    'item_name': item_name,
                    'lower_case_name': item_name.lower(),
                    'category': category,
                    'price': price,
                    'last_updated_at': last_updated_at
                },
                ReturnValues="ALL_OLD"
            )
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                },
                'body': json.dumps({'id': item_id})
            }
        except ClientError as e:
            return {
                'statusCode': 500,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type',
                },
                'body': json.dumps('Error inserting/updating item: {}'.format(e.response['Error']['Message']))
            }
