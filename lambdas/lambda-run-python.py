import json
import boto3
import os 
import sys
from io import StringIO
import contextlib
import os.path,subprocess
from subprocess import STDOUT,PIPE
import logging
from botocore.exceptions import ClientError
import uuid

lambda_client = boto3.client('lambda') 
s3_client = boto3.client('s3')
sqs_client = boto3.client('sqs')
dynamo = boto3.resource('dynamodb')

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

def create_file(file_name,lang_extension,code_body):
    os.chdir('/tmp')
    file_full_name = file_name+"."+lang_extension
    with open(file_full_name, "w") as f:
        f.write(code_body)
    f.close()

def invoke_lambda(event,function_arn):
    response = lambda_client.invoke(
        FunctionName = function_arn,
        InvocationType = 'RequestResponse',
        Payload = json.dumps(event)
    )
    
    function_response = json.load(response['Payload'])
    return function_response


def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def send_sqs_message(messageBody,code_language,code_id):
    sqs_response = sqs_client.send_message(QueueUrl=sqs_client.get_queue_url(QueueName=os.environ["SQS_QUEUE_NAME"])["QueueUrl"],MessageBody=code_id, MessageAttributes={
    'Lang': {
        'StringValue': code_language,
        'DataType': 'String'
    }
    })
    print ("SQS Response:",sqs_response)

def add_dynamo_item(code_id,status):
    table = dynamo.Table(os.environ["CODE_TABLE"])
    item = {
        'codeID':code_id,
        'completion_status':status,
    }
    table.put_item(Item=item)
    
def lambda_handler(event, context):
    # TODO implement
    
    code = event["body"]
    print ("Event",event)
    lang_extension = event["queryStringParameters"]["language"]
    codeOutput = ""
    
    if (lang_extension=="js"):
        lambda_response = invoke_lambda(event,os.environ["JAVASCRIPT_LAMBDA_ARN"])
        codeOutput = lambda_response["out"]
        print ('Javascript Response',codeOutput)
    elif (lang_extension=="py"):
        with stdoutIO() as s:
            try:
                exec(code)
            except:
                print("Code Has Compilation Error")

        print("Code Output:", s.getvalue())
        codeOutput = s.getvalue()
    elif  (lang_extension=="java" or lang_extension=="cpp" or lang_extension=="go"):
        code_id = str(uuid.uuid4()) # Code Id from random uuid generator
        print ("Random Code ID: ",code_id)
        create_file("test",lang_extension,code)
        upload_success = upload_file("test"+"."+lang_extension,os.environ['MOUNTED_BUCKET_NAME'],'input/'+code_id+'.'+lang_extension)
        print ("Uploaded File to Mount Bucket Succesfully",upload_success)
    
        print ("Sending Message To Queue")
        send_sqs_message(code,lang_extension,code_id)
    
        print ("Adding to Dynamo Table with Code Initialized Status")
        status = "Initialized"
        add_dynamo_item(code_id,status)
        codeOutput = code_id 
    else:
        print ("Choose a valid language")
    return {
        'statusCode': 200,
        'headers':{
            'Access-Control-Allow-Origin' : '*',
            'Access-Control-Allow-Methods': '*',
            'Access-Control-Allow-Headers': '*',
            'Content-Type': 'application/json'
        },
        'body': codeOutput
    }
