import json
import boto3
import os
from boto3.dynamodb.conditions import Key, Attr
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])

        # Extract filters, pagination, and sort options
        filters = body.get('filters', {})
        pagination = body.get('pagination', {})
        sort = body.get('sort', {})

        name_filter = filters.get('name')
        category_filter = filters.get('category')
        price_range = filters.get('price_range')
        print(filters.get('price_range'))

        page = pagination.get('page', 1)
        limit = pagination.get('limit', 10)

        sort_field = sort.get('field', 'price')
        sort_order = sort.get('order', 'asc')

        # Build the filter expression
        filter_expression = None

        if name_filter is not None:
            if name_filter.strip() != "":
                filter_expression = Attr('lower_case_name').contains(
                    str(name_filter).lower())
        # if name_filter:
        #     filter_expression = Attr(
        #         'lower_case_name').contains(str(name_filter).lower())

        if category_filter:
            if filter_expression:
                filter_expression &= Attr('category').eq(category_filter)
            else:
                filter_expression = Attr('category').eq(category_filter)
        if price_range:
            if filter_expression:
                filter_expression &= Attr('price').between(
                    Decimal(price_range[0]), Decimal(price_range[1]))
            else:
                filter_expression = Attr('price').between(
                    Decimal(price_range[0]), Decimal(price_range[1]))

        # Set up the scan parameters
        scan_params = {
            # 'FilterExpression': filter_expression,
            'Limit': limit
        }
        if filter_expression:
            scan_params['FilterExpression'] = filter_expression

        # Perform the scan operation
        response = table.scan(**scan_params)

        items = response['Items']

        # Sort the items
        reverse = sort_order == 'desc'
        sorted_items = sorted(items, key=lambda x: Decimal(
            x[sort_field]), reverse=reverse)

        # Format the response
        result = {
            'items': sorted_items[:limit]
        }

        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps(result, default=str)
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps(f"Error processing request: {str(e)}")
        }
