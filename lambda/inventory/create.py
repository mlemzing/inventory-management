import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(
    "ItemCdkStackDatabaseStackC8E485B5-InventoryTableFD135387-1NMBHG6644689")


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
