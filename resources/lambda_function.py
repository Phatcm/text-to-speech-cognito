import json
import boto3
import os
import uuid

polly = boto3.client('polly')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    body = json.loads(event["body"])
    text = body["text"]
    
    

    file_name = generateAudioUsingText(text)
    url = generatePresignUrl(file_name)

    return {
        'statusCode': 200,
        'body': json.dumps(url)
    }

def generateAudioUsingText(text):
    try:
        response = polly.synthesize_speech( Text=text,
                                            Engine="standard",
                                            TextType = "text",
                                            OutputFormat="mp3",
                                            SampleRate='22050',
                                            VoiceId="Matthew")
        
        #define bucket connect
        bucket_name = os.environ['BUCKET_NAME']
        
        file_name = str(uuid.uuid4())+".mp3"
        stream = response["AudioStream"]
        
        s3.put_object(Bucket = bucket_name, Key=file_name, Body=stream.read())
        return file_name # Return the file_name if it is successfully generated
    except Exception as e:
        print(e)
        return None # Return None and print the exception
    
def generatePresignUrl(file_name):
    try:
        url = s3.generate_presigned_url('get_object',
                                                Params={'Bucket': os.environ['BUCKET_NAME'],'Key': file_name},
                                                ExpiresIn=3600)
        return url  # Return the URL if it is successfully generated
    except Exception as e:
        print(e)
        return None  # Return None and print the exception