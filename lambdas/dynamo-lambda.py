import json
import boto3
import os

dynamodb_client = boto3.resource('dynamodb')
s3_client = boto3.client('s3')
def lambda_handler(event, context):
    # TODO implement
    code_id = event["queryStringParameters"]["code_id"]
    print ("Code Id: ",code_id)
    table = dynamodb_client.Table(os.environ['CODE_TABLE'])
    response = response = table.get_item(
        Key={
            'codeID': code_id,
        }
        )
    print (response)
    code_id_status = response["Item"]["completion_status"]
    
    lambda_response = ""
    if (code_id_status == "Initialized"):
        lambda_response = "Still running the code"
    elif (code_id_status == "Complete"):
        s3_client.download_file(os.environ['MOUNTED_BUCKET_NAME'],'output/'+code_id+'.txt','/tmp/output.txt')
        with open('/tmp/output.txt') as f:
            output = f.readlines()
        lambda_response = ' '.join(output)
    else:
        pass
    
    return {
        'statusCode': 200,
        'headers':{
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Headers': '*',
            'Content-Type': 'application/json'
        },
        'body': lambda_response
    }
