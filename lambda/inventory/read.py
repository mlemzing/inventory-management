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
    dt_from = event['queryStringParameters']['dt_from']
    dt_to = event['queryStringParameters']['dt_to']

    # Convert to datetime objects
    start_date = datetime.strptime(dt_from, "%Y-%m-%d %H:%M:%S")
    end_date = datetime.strptime(dt_to, "%Y-%m-%d %H:%M:%S")

    # Convert to ISO format
    start_date_iso = start_date.isoformat()
    end_date_iso = end_date.isoformat()

    # Perform a scan operation with the specified date range
    response = table.scan(
        FilterExpression=boto3.dynamodb.conditions.Key('last_updated_at').between(
            start_date_iso, end_date_iso),
        Limit=10
    )

    # Convert the response to JSON serializable format
    items = response['Items']
    result = []
    sum = 0
    for item in items:
        result.append({
            'id': item['id'],
            'name': item['item_name'],
            'category': item['category'],
            'price': str(item['price'])
        })
        sum += item['price']

    # Return the results
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
        'body': json.dumps({'items': result, 'total_price': float(sum)})
    }
