import json
from datetime import datetime
import os
import boto3

cognito_client = boto3.client('cognito-idp')

def list_users(event, context):
    
    if 'UserPoolId' not in event:
        raise KeyError("UserPoolId does not exist.")
    
    response = cognito_client.list_users(
        UserPoolId = event['UserPoolId']
    )

    return json.dumps(response, default=support_datetime_default)

def support_datetime_default(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(repr(obj) + " is not JSON serializable")