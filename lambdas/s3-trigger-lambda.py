import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    # TODO implement
    print ("S3 works")
    print (event)
    print (context)
    object_key = event["Records"][0]["s3"]["object"]["key"]
    code_id = object_key.split("/")[1].replace(".txt","")
    
    print ("Code Id:",code_id)
    print ("Object Key:",object_key)
    
    table = dynamodb.Table(os.environ['CODE_TABLE'])
    
    table.update_item(
        Key={'codeID': code_id},
        UpdateExpression="set completion_status=:newStatus",
        ExpressionAttributeValues={
            ":newStatus": "Complete"
        },
        ReturnValues="UPDATED_NEW"
    )
    
    response = table.get_item(
        Key={
            'codeID': code_id,
        }
        )
    print ("Dynamo Response: ",response)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
