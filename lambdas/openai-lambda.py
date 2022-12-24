import json
import os
import openai

def lambda_handler(event, context):
    # TODO implement
    print (event)
    prompt = event["queryStringParameters"]
    
    openai.api_key = os.environ["OPENAI_API_KEY"]

    response = openai.Completion.create(
        model="code-davinci-002",
        prompt = prompt,
        temperature=0,
        max_tokens=64,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["\"\"\""]
    )

    openai_response = response["choices"][0]["text"]
    print ("Open AI Response",openai_response)
    
    return {
        'statusCode': 200,
        'body': openai_response
    }
