import json
import boto3
from datetime import datetime
import hashlib
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
import os

def lambda_handler(event, context):
    # TODO implement
    print(event)
    for i in os.walk('/opt'):
        print(i)
    # access_token = 'eyJraWQiOiJRUnRUM1doNm55VUpMaG11Y3BnVDBaekdmMTd1RG1lMkh5c2tcL3hsSlpVST0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJiZWZjMDk4Ny1jZTU4LTRhZjMtYWEzZS0xZjJkMjFlY2I1MTAiLCJldmVudF9pZCI6IjU1YWRlNTFiLWFiNTAtNDFiYy1hNGZjLWNjYWE1Yjg5MjM5NSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4gcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE1NzY3MDU1NDksImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX3dQanB4M21sNCIsImV4cCI6MTU3NjcwOTE0OSwiaWF0IjoxNTc2NzA1NTQ5LCJ2ZXJzaW9uIjoyLCJqdGkiOiJhMTFkNGU1NC01YzBlLTQ3ZjYtODllOS1iZWNiZjc4M2Y1MTIiLCJjbGllbnRfaWQiOiI3cjJpaTRqcmhyN202MTZ2dHVqNHFnMmdnYyIsInVzZXJuYW1lIjoiYmVmYzA5ODctY2U1OC00YWYzLWFhM2UtMWYyZDIxZWNiNTEwIn0.jYLewKZuh56aHYA5VxgFTPQdTZg2FSwryVjv05SDekh3x_iboz3Tqwd_PxcjJzIa91F2QOxCDalxpS1DNtTUDK68CghDtX4-5KoEH7eELYj_2ki2cfdvlZVlJ_0fX9097SyAwyWw_R9A3f7Vcv9Bjbqi1zTx39EemoPLHUJGiWJi9muRSFrjb9_5wrWYol2ResWjd9qO9tYfxU0jq-07EkP45r6A0u_9dbfntovmy72Zh0en-OP5V5GE2C4iHkM-ZWwS52pr2bhVWMRpqJb3sedE5DtyTsy2mSIDTX-GGZog2kArd2EKWHe_psYQNjIHFqRuQDQirwJYJykK4FZRCg'
    # client = boto3.client('cognito-idp')
    # response = client.delete_user(
    #     AccessToken = access_token
    #     )
    # print(response)
    # email = 'hardikaj96@gmail.com'
    # mobile_number = '+15512288614'
    # first_name = 'Hardik'
    # last_name = 'Jivani'
    # password = 'hardik1234'
    # plan = 'starter'
    # em = email.split('@')[0]
    # em1 = email.split('@')[1].split('.')
    # m = hashlib.md5()
    # m.update(em.encode('utf8'))
    # m.update(em1[0].encode('utf8')+em1[1].encode('utf8'))
    # user_id = m.hexdigest()
    # if check_user(user_id):
    #     return {
    #     'statusCode': 200,
    #     'body': json.dumps('user with email '+email+' exists in the system')
    #     }
    # put_user(user_id, email, mobile_number, first_name, last_name, password, plan)
    # client = boto3.client('ses',
    # aws_access_key_id='AKIAX7DBGCU3GJHQZBNU',
    # aws_secret_access_key='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')
    # response = client.send_email(
    #     Source='hardikaj96@gmail.com',
    #     Destination={
    #         'ToAddresses': [
    #             'satishagr@gmail.com',
    #         ]
    #     },
    #     Message={
    #         'Subject': {
    #             'Data': 'Welcome MyMacroChef'
    #         },
    #         'Body': {
    #             'Text': {
    #                 'Data': 'Welcome to MyMacroChef'
    #             }
    #         }
    #     }
    # )
    # print(response)
    return {
        'statusCode': 200,
        'body': json.dumps('user added successfully')
    }

def check_user(user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_details')
    response = table.get_item(
        Key={
            'user_id': user_id
        }
    )
    if 'item' in response:
        print("GetItem succeeded:")
        print(json.dumps(item, indent=4))
        return True
    print(json.dumps(response, indent=4))
    return False
    
def put_user(user_id, email, mobile_number, first_name, last_name, password, plan):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_details')
    response = table.put_item(
        Item={
        'user_id' : user_id,
        'email': email,
        'mobile_number': mobile_number,
        'first_name': first_name,
        'last_name': last_name,
        'password': password,
        'plan': plan,
        'created_at': datetime.utcnow().isoformat()
        }
    )
    print("PutItem succeeded:")
    print(json.dumps(response, indent=4))