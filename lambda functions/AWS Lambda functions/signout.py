import json
import boto3
from datetime import datetime
import hashlib
from boto3.dynamodb.conditions import Key, Attr
import decimal

s3 = boto3.client('s3')
def lambda_handler(event, context):
    # TODO implement
    print(event)
    # email = 'hardikaj96@gmail.com'
    # em = email.split('@')[0]
    # em1 = email.split('@')[1].split('.')
    # m = hashlib.md5()
    # m.update(em.encode('utf8'))
    # m.update(em1[0].encode('utf8')+em1[1].encode('utf8'))
    # print(m.hexdigest())
    # user_id = m.hexdigest()
    # signout_user(user_id)
    # user_id = 'f14db0e21dd06e32f8ce24ff67a8b7a4'
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_profile')
    response = table.scan(
    )
    print(response)
    # client = boto3.client('apigateway')
    # response = client.get_rest_apis()
    # print(response['items'])
    # clusterfile = s3.get_object(Bucket='mymacrochefhj', Key='Resources/Data/data.json')
    # print(clusterfile)
    # clusterDF = pd.read_json(clusterfile['Body'])
    # print(clusterDF.head())
    return {
        'statusCode': 200,
        'body': json.dumps({
            'res' :'user signed out successfully',
            'token':'as'
            }
            )
        }
    
# def signout_user(user_id):
#     dynamodb = boto3.resource('dynamodb')
#     table = dynamodb.Table('login')
#     response = table.delete_item(
#         Key={
#             'user_id': user_id
#         }
#     )
#     print("Delete Item succeeded:")
#     print(json.dumps(response, indent=4))

import json
import hashlib
import boto3
from botocore.vendored import requests

def lambda_handler(event, context):
    # TODO implement
    print(event)
    if 'queryStringParameters' in event:
        access_token = event['queryStringParameters']['user_id']
    else:
        access_token = "eyJraWQiOiJRUnRUM1doNm55VUpMaG11Y3BnVDBaekdmMTd1RG1lMkh5c2tcL3hsSlpVST0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJlZDI3YzU1Ni0wYzU0LTQ4YmMtOWU5Mi0yMTRhOTY1YmQxZGEiLCJldmVudF9pZCI6IjFkOGFjOTZmLTk3ODEtNDFlYS04NjlhLWVlMzNkZjJmZDBkOSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4gcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE1NzY0NTA2NjAsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX3dQanB4M21sNCIsImV4cCI6MTU3NjQ1NDI2MCwiaWF0IjoxNTc2NDUwNjYwLCJ2ZXJzaW9uIjoyLCJqdGkiOiJmZTVlMDNiZS03ZTFkLTRjZWYtODQ3Zi03NTVjODUyNTQ0NWQiLCJjbGllbnRfaWQiOiI3cjJpaTRqcmhyN202MTZ2dHVqNHFnMmdnYyIsInVzZXJuYW1lIjoiZWQyN2M1NTYtMGM1NC00OGJjLTllOTItMjE0YTk2NWJkMWRhIn0.J4D3L7H8Bgt07p7aElxmlzT63Bw9JU4ou6urGDs7bHb67Alr_zmzrT12FQyLmWy2mdRNAk6EypWq2OzJ9V7vvp1ZfbMR4nzR2wkS0JyXO116Od9DgNmGsujmur54zDFPCA8-cXSzghj91yLJCmdYF6-yshKQQ8nNi_ZpsgPvF4NnFy7n9mcOtpkPE18BmQM4sTbmsPJmd_nt9PahHbvoGZ_Mp7hbeY4kWMv22MbMO5H07PZCeZawjwJDw3SXwfdLimNj8ySfYHHjhEedKdeebqCZ-dXhaAm9OAjr5FTYFLg2intOueKvA5DTd8rNRyhskSH_ZHvPW8GdbkJwd-7ChA"
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
        email = 'hardikaj96@gmail.com'
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

    
def put_user_profile(user_id, completion_level):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_profile')
    response = table.put_item(
        Item={
        'user_id' : user_id,
        'completion_level': completion_level
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