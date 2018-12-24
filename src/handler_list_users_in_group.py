import json
from datetime import datetime
import os
import boto3

cognito_client = boto3.client('cognito-idp')

def list_users_in_group(event, context):
    event = event['queryStringParameters']
    
    if 'UserPoolId' not in os.environ:
        raise KeyError("UserPoolId does not exist in environment variable.")
    if 'GroupName' not in event:
        raise KeyError("GroupName does not exist.")
    
    res_users = cognito_client.list_users_in_group(
        UserPoolId = os.environ['UserPoolId'],
        GroupName = event['GroupName']
    )

    user_jsons = json.loads(json.dumps(res_users, default=support_datetime_default))
    

    for user_json in user_jsons['Users']:
        group_res = cognito_client.admin_list_groups_for_user(
            UserPoolId = os.environ['UserPoolId'],
            Username = user_json['Username']
        )
        
        # print(group_res)
        group_json = json.loads(json.dumps(group_res, default=support_datetime_default))
        if len(group_json['Groups']) > 0:
          user_json['Groups'] = list(filter(lambda x: x, group_json['Groups']))

    return {
        'statusCode': 200,
        'headers': {
        "Access-Control-Allow-Origin" : "*"
        },
        'body': json.dumps(user_jsons)
    }

def support_datetime_default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(repr(obj) + " is not JSON serializable")