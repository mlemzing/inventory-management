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
    category = event['queryStringParameters']['category']

    # Perform a scan operation with the specified date range
    if category == 'all':
        # Scan the table to get all items
        response = table.scan()
        items = response['Items']
    else:
        # Query the table using the CategoryIndex
        response = table.query(
            IndexName='CategoryIndex',
            KeyConditionExpression=boto3.dynamodb.conditions.Key(
                'category').eq(category)
        )
        items = response['Items']

    # Aggregate the results by category
    category_aggregates = {}
    for item in items:
        cat = item['category']
        price = Decimal(item['price'])
        if cat not in category_aggregates:
            category_aggregates[cat] = {'total_price': price, 'count': 1}
        else:
            category_aggregates[cat]['total_price'] += price
            category_aggregates[cat]['count'] += 1

    # Format the response
    result = []
    for cat, data in category_aggregates.items():
        result.append({
            'category': cat,
            'total_price': float(data['total_price']),
            'count': data['count']
        })

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
        'body': json.dumps({'items': result})
    }
