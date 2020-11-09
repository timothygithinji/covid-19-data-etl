import json
import pandas as pd
from io import StringIO
import boto3
import data

def hello(event, context):
    # Data Module
    df = data.main()

    # Save to S3
    bucket = 'covid-19-data-etl-timothygithinji'
    
    # Covert dataframe to CSV
    csv_buffer = StringIO()
    df.to_csv(csv_buffer, encoding='utf-8', header=False, index=False)

    # S3 Client
    s3_resource = boto3.resource('s3')
    s3_resource.Object(bucket, 'data/data.csv').put(Body=csv_buffer.getvalue())
    
    # SNS Client
    sns = boto3.client('sns')
    topic_arn = 'arn:aws:sns:us-east-1:144272576793:covid-19-etl-SNS'
    message = 'New data saved to S3 bucket'
    sns.publish(TopicArn=topic_arn,Message=message)

    return {
        "message": "New data saved to S3 bucket"
    }