import json
import boto3
import os 

sqs_client = boto3.client('sqs')
ssm_client = boto3.client('ssm')

def lambda_handler(event, context):
    # TODO implement
    instance_id = os.environ["EC2_INSTANCE_ID"]
    
    command = 'python3 /SQS_cron.py'
    ssmresponse = ssm_client.send_command(InstanceIds=[instance_id,], DocumentName='AWS-RunShellScript', Parameters= { 'commands': [command] ,} ) 
    print ("SSM Response",ssmresponse)
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
