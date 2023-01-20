# BroCode - Cloud Based IDE to quickly prototype code
Cloud Computing(CS-GY 9223) Final Project


### Description
Our aim is to create a Cloud Based IDE which will quickly execute your code by providing you compilers for many different languages on the Cloud. This can also be used by people who do not want to go through the hastle of setting up environments. 


#### PS: Due to free tier limits we had to shut our instances down 


### List of AWS Services
- Lambda
- Amazon Simple Storage Service (S3)
- Amazon Elastic Compute Cloud (EC2)
- Amazon Simple Queue Service (SQS)
- Amazon Cognito
- DynamoDB
- AWS Systems Manager Agent (SSM)
- API Gateway

### Service Flow
- User logs in with Cognito

- They write some code in the frontend and select the language, they click on the Run button which triggers a PUT request.

- First Lambda Function receives the request, it adds the code body and assigns a random uuid generator to it. It also creates a file with the code in the input directory of S3.

- We add this message to an SQS queue and also add the code id to Dynamo along with a state of “Initialized”.

- The SQS Event triggers the second Lambda function which calls a Python script on the Amazon EC2 instance via the AWS SSM Agent.

- The script reads the language and accordingly runs the relevant Docker container. The output is saved to the output directory of S3.

- A put event in the output directory of S3 triggers the third Lambda function which updates the DynamoDB with the relevant id and the status as “Completed”

- After this the fourth Lambda function continuously checks Dynamo for the requested Code ID and its status. If it determines that the code is “Completed” then it reads the output S3 object to a temp directory and returns the output to the frontend(code editor).

### Open AI API for Code Completion

We also utilized the Davinci model of Open AI Completion API for the task of Automatic Code Completion.
User gives a prompt on the code editor and calls the Code Complete which triggers a request to the Open API Completion API and returns the completed prompt.
This is a really helpful feature especially for programmers who are beginners.



### Architecture
![alt text](https://github.com/zuther77/Brocode/blob/master/images/Project_Architecture.jpeg)
