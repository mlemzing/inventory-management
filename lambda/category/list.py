from decimal import Decimal
import json
import boto3
import os
import uuid
import boto3.dynamodb
import boto3.dynamodb.conditions
from botocore.exceptions import ClientError
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(
    table_name)


# Get distinct categories
def lambda_handler(event, context):
    response = table.scan(
        IndexName='CategoryIndex',
        ProjectionExpression='category'
    )

    items = response['Items']
    unique_categories = set(item['category'] for item in items)

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
        'body': json.dumps({
            'unique_categories': list(unique_categories)
        })
    }
