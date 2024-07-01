import json
import boto3
import os
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def create_todo(event, context):
    body = json.loads(event['body'])
    todo_id = body['id']
    title = body['title']
    description = body['description']

    item = {
        'id': todo_id,
        'title': title,
        'description': description
    }
    table.put_item(Item=item)

    return {
        'statusCode': 201,
        'body': json.dumps({'message': 'To-Do item created successfully'})
    }

def get_todo(event, context):
    todo_id = event['pathParameters']['id']

    response = table.get_item(Key={'id': todo_id})
    item = response.get('Item')

    if item:
        return {
            'statusCode': 200,
            'body': json.dumps(item)
        }
    else:
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'To-Do item not found'})
        }

def update_todo(event, context):
    todo_id = event['pathParameters']['id']
    body = json.loads(event['body'])

    update_expression = "set title = :title, description = :description"
    expression_attribute_values = {
        ':title': body['title'],
        ':description': body['description']
    }

    table.update_item(
        Key={'id': todo_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_attribute_values
    )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'To-Do item updated successfully'})
    }

def delete_todo(event, context):
    todo_id = event['pathParameters']['id']

    table.delete_item(Key={'id': todo_id})

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'To-Do item deleted successfully'})
    }
