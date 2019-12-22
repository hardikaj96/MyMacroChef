import json
import hashlib
import boto3
from botocore.vendored import requests

def lambda_handler(event, context):
    # TODO implement
    print(event)
    if 'queryStringParameters' in event:
        access_token = event['queryStringParameters']['user_id']
        print('access_token received')
    else:
        access_token = "eyJraWQiOiJRUnRUM1doNm55VUpMaG11Y3BnVDBaekdmMTd1RG1lMkh5c2tcL3hsSlpVST0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJlZDI3YzU1Ni0wYzU0LTQ4YmMtOWU5Mi0yMTRhOTY1YmQxZGEiLCJldmVudF9pZCI6IjM0NDcxMjY1LWI1YTktNGE3MC1hNDVmLTlhZTI4ZmJlY2I5NyIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4gcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE1NzY2NTIzNTEsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX3dQanB4M21sNCIsImV4cCI6MTU3NjY1NTk1MSwiaWF0IjoxNTc2NjUyMzUxLCJ2ZXJzaW9uIjoyLCJqdGkiOiI2OThlYWFmOC0wZTNjLTQyZGUtOWI1NS0wY2JlNjM1YjE1MGMiLCJjbGllbnRfaWQiOiI3cjJpaTRqcmhyN202MTZ2dHVqNHFnMmdnYyIsInVzZXJuYW1lIjoiZWQyN2M1NTYtMGM1NC00OGJjLTllOTItMjE0YTk2NWJkMWRhIn0.c9U2wAx-oncoGgcWOTXWkF58MYYW-bk4jIOfsRXuXlCdci4MqPdBBEVHMXloF-BJSii0WawX4CosnnCs14FIHdZqsLshYrt_rfZeTkTKs3KYt2Oh5GDyt74Alw1dBqYlutYFB5djqznkcaLRFMjvhy0hRe8dPDwsMpxcKf8N2R1VmnlBEmhJYrpqF2RaiVDpPShfW4AsEK8vokyV9RjXnlZYphfyxvzUwGzVT0KoKBa5tCVFQ0hLrD7J5rtJt5TcyTwwGeZhWmEwtfAlEUKbgpP-etZS6m875Ll3qfLvxQJEvarzyZOzIe4ocbqhCHG591raQLqfPYyBDclI2Kmndg"
    headers = {
			'Authorization': 'Bearer ' + access_token,
			'Content-Type': 'application/x-www-form-urlencoded'
		  }
    payload={}
    url = 'https://planmeal.auth.us-east-1.amazoncognito.com/oauth2/userInfo'
    r = requests.get(url, data=json.dumps(payload), headers=headers)
    print(r.json())
    if 'email' in r.json():
        email = r.json()['email']
    else:
        return {
            'statusCode': 200,
            'headers':{
                'Access-Control-Allow-Origin':'*',
                'Access-Control-Allow-Credentials':True
            },
                'body': json.dumps({
                    'invalid_access_token':'1'
            })
        }
    print(email)
    em = email.split('@')[0]
    em1 = email.split('@')[1].split('.')
    m = hashlib.md5()
    m.update(em.encode('utf8'))
    m.update(em1[0].encode('utf8')+em1[1].encode('utf8'))
    print(m.hexdigest())
    user_id = m.hexdigest()
    item = check_user_profile(user_id)
    add_active_user(user_id)
    send_email(email)
    if not item:
        put_user_profile(user_id, '0', email)
        print('user_profile found')
        return {
            'statusCode': 200,
        'headers':{
            'Access-Control-Allow-Origin':'*',
            'Access-Control-Allow-Credentials':True
        },
            'body': json.dumps({
                'user_id':user_id,
                'page_num':'0'
            })
        }
    else:
        return {
            'statusCode': 200,
        'headers':{
            'Access-Control-Allow-Origin':'*',
            'Access-Control-Allow-Credentials':True
        },
            'body': json.dumps(item)
        }

def check_user_profile(user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_profile')
    response = table.get_item(
        Key={
            'user_id': user_id
        }
    )
    if 'Item' in response:
        item = response['Item']
        print("Get profile succeeded:")
        print(item)
        return item
    # print(json.dumps(response, indent=4))
    return None

    
def put_user_profile(user_id, completion_level, email):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_profile')
    response = table.put_item(
        Item={
        'user_id' : user_id,
        'completion_level': completion_level,
        'email': email
        }
    )
    print("PutItem succeeded:")
    print(json.dumps(response, indent=4))
    

def add_active_user(user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_active')
    response = table.scan()
    print(response)
    if response['Count'] != 0:
        delete_active_user(response['Items'])
    response = table.put_item(
        Item={
            'user_id':user_id
            
        })
    print(response)
    
def delete_active_user(items):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_active')
    print(items)
    for item in items:
        response = table.delete_item(
          Key={
                    'user_id': item['user_id']
                }
            )
        print(response)
        
def send_email(email):
    client = boto3.client('ses',
    aws_access_key_id='AKIAX7DBGCU3GJHQZBNU',
    aws_secret_access_key='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')
    response = client.send_email(
        Source='hardikaj96@gmail.com',
        Destination={
            'ToAddresses': [
                email,
            ]
        },
        Message={
            'Subject': {
                'Data': 'MyMacroChef'
            },
            'Body': {
                'Text': {
                    'Data': 'Welcome to MyMacroChef\n Please fill out your profile to achieve maximum rewards.!!!'
                }
            }
        }
    )
    print(response)