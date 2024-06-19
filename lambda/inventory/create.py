import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(
    table_name)


def lambda_handler(event, context):
    table.put_item(
        Item={
            'id': '1',  # Partition key
            'last_updated_dt': '2024-06-18T16:49:18.132Z',  # Sort key
            'item_name': 'test'
        }
    )

    return {
        'statusCode': 200,
        'body': json.dumps("Hello from lambda")
    }
