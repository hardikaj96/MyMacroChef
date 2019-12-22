import json
import hashlib
import boto3

def lambda_handler(event, context):
    # TODO implement
    print(event)
    email = 'hardikaj96@gmail.com'
    em = email.split('@')[0]
    em1 = email.split('@')[1].split('.')
    m = hashlib.md5()
    m.update(em.encode('utf8'))
    m.update(em1[0].encode('utf8')+em1[1].encode('utf8'))
    print(m.hexdigest())
    user_id = m.hexdigest()
    if check_user(user_id):
        insert_into_login(user_id)
        return {
        'statusCode': 200,
        'body': json.dumps({
            'res' :'signin succeeded',
            'token':user_id
            }
            )
        }
    return {
        'statusCode': 200,
        'body': json.dumps('user not found')
    }

def check_user(user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_details')
    response = table.get_item(
        Key={
            'user_id': user_id
        }
    )
    if 'Item' in response:
        item = response['Item']
        print("GetItem succeeded:")
        print(json.dumps(item, indent=4))
        return True
    print(json.dumps(response, indent=4))
    return False
    
def insert_into_login(user_id):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('login')
    response = table.put_item(
        Item={
        'user_id' : user_id
        }
    )
    print("PutItem succeeded:")
    print(json.dumps(response, indent=4))