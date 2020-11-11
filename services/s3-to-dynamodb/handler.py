import boto3
import csv

def hello(event, context):
    # Empty list to append CSV rows
    statistics_list = []

    # S3 Client
    s3 = boto3.client('s3')

    # DynamoDB Client
    region = 'us-east-1'         
    dynamodb = boto3.client('dynamodb', region_name=region)
    
    try:
        # Get data.csv object from S3 bucket
        data = s3.get_object(Bucket='covid-19-data-etl-timothygithinji', Key='data/data.csv')
        statistics_list = data['Body'].read().decode('utf-8').split('\n')
        csv_reader = csv.reader(statistics_list, delimiter=',', quotechar='"')

        for row in csv_reader:
            date = row[0]
            cases = row[1]
            deaths = row[2]
            recovered = row[3]

            # Put each row into DynamoDB Table
            response = dynamodb.put_item(
                TableName = 'covid-19-data-etl',
                Item = {
                'date' : {'S':str(date)},
                'cases': {'N':str(cases)},
                'deaths': {'N':str(deaths)},
                'recovered': {'N':str(recovered)},
                }
            )
    except Exception as e:
        # Last row of CSV Blank Execption catch
        print(str(e))

    # SNS Client - Message Publish
    sns = boto3.client('sns')
    topic_arn = 'arn:aws:sns:us-east-1:144272576793:covid-19-data-etl'
    message = 'New Data insert into DynamoDB Table'
    sns.publish(TopicArn=topic_arn, Message=message)

    return {
        "message": "New Data insert into DynamoDB Table",
    }