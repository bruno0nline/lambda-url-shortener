import json
import os
import boto3
import hashlib
from datetime import datetime, timedelta

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def handler(event, context):
    method = event['requestContext']['http']['method']
    
    if method == 'POST':
        return shorten_url(event)
    elif method == 'GET':
        return redirect_url(event)
    
    return {'statusCode': 405, 'body': json.dumps({'error': 'Method not allowed'})}

def shorten_url(event):
    try:
        body = json.loads(event.get('body', '{}'))
        url = body.get('url')
        
        if not url:
            return {'statusCode': 400, 'body': json.dumps({'error': 'URL required'})}
        
        # Gera ID curto usando hash
        short_id = hashlib.md5(url.encode()).hexdigest()[:6]
        
        # Expira em 30 dias
        expires_at = int((datetime.now() + timedelta(days=30)).timestamp())
        
        table.put_item(Item={
            'short_id': short_id,
            'url': url,
            'created_at': datetime.now().isoformat(),
            'expires_at': expires_at
        })
        
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'short_id': short_id, 'expires_in_days': 30})
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}

def redirect_url(event):
    try:
        short_id = event['pathParameters']['short_id']
        
        response = table.get_item(Key={'short_id': short_id})
        
        if 'Item' not in response:
            return {'statusCode': 404, 'body': json.dumps({'error': 'URL not found'})}
        
        url = response['Item']['url']
        
        return {
            'statusCode': 301,
            'headers': {'Location': url},
            'body': ''
        }
    except Exception as e:
        return {'statusCode': 500, 'body': json.dumps({'error': str(e)})}
