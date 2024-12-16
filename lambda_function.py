import boto3
import json
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('todos')

def get_id():
    id = uuid.uuid4()
    return str(id)  

def lambda_handler(event, context):
    http_method = event["httpMethod"]
    path = event.get('path', '')
    headers = {
        'Access-Control-Allow-Origin': '*', 
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS', 
        'Access-Control-Allow-Headers': 'Content-Type',  
    }
    
    # Fetch all items
    if http_method == "GET" and path == '/items':
        count = table.scan()
        items = count.get('Items', [])
        response = {
            "statusCode": 200,
            "headers": headers,
            "body": json.dumps(items)
        }
        return response
    
    # Create new item
    elif http_method == "POST" and path == '/items':
        item_id = get_id()  
        data = json.loads(event['body'])  

        if 'title' not in data:
            response = {
               "statusCode": 400, 
               "headers": headers,
               "body": json.dumps({"message": "'title' field is required"})
            }
            return response 

        data['id'] = item_id
        table.put_item(Item=data)

        response = {
           "statusCode": 200,
           "headers": headers,
           "body": json.dumps({"message": "Item added or posted"})
        }
        return response

    # Delete all items
    elif http_method == "DELETE" and path == '/items':
        count = table.scan()
        items = count.get('Items', [])
        for item in items:
            table.delete_item(Key={'id': item['id']})
        response = {
           "statusCode": 200,
           "headers": headers,
           "body": json.dumps({"message": "all items deleted"})
        }
        return response
    
    # Update item by id
    elif http_method == "PUT" and path.startswith('/items/'):
        item_id = path.split('/')[-1]  
        data = json.loads(event['body']) 
        if 'title' not in data:
            response = {
               "statusCode": 400, 
               "headers": headers,
               "body": json.dumps({"message": "'title' field is required"})
            }
            return response 
        data['id'] = item_id 
        table.put_item(Item=data)

        response = {
           "statusCode": 200,
           "headers": headers,
           "body": json.dumps({"message": "Item updated"})
        }
        return response
        
    # Get item by id
    elif http_method == "GET" and path.startswith('/items/'):
        item_id = path.split('/')[-1]
        data = table.get_item(Key={"id": str(item_id)})
        item = data.get("Item")
        if item is not None:
            response = {
               "statusCode": 200,
               "headers": headers,
               "body": json.dumps(item)
            }
            return response
        else:
            response = {
               "statusCode": 404,
               "headers": headers,
               "body": json.dumps({"message": "Item not found"})
            }
            return response
            
    # Delete item by id
    elif http_method == "DELETE" and path.startswith('/items/'):
        item_id = path.split('/')[-1]  
        table.delete_item(Key={'id': item_id})
        response = {
           "statusCode": 200,
           "headers": headers,
           "body": json.dumps({"message": "Item deleted"})
        }
        return response
