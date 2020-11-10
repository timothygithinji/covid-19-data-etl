import boto3
import csv

def hello(event, context):
    region = 'us-east-1'
    recList = []           
    s3 = boto3.client('s3')            
    dyndb = boto3.client('dynamodb', region_name=region)
    
    try:
        confile = s3.get_object(Bucket='covid-19-data-etl-timothygithinji', Key='data/data.csv')
        recList = confile['Body'].read().decode('utf-8').split('\n')
        csv_reader = csv.reader(recList, delimiter=',', quotechar='"')

        for row in csv_reader:
            date = row[0]
            cases = row[1]
            deaths = row[2]
            recovered = row[3]
            response = dyndb.put_item(
                TableName = 'covid-19-etl',
                Item = {
                'date' : {'S':str(date)},
                'cases': {'N':str(cases)},
                'deaths': {'N':str(deaths)},
                'recovered': {'N':str(recovered)},
                }
            )
    except Exception as e:
        print(str(e))

    sns = boto3.client('sns')
    topic_arn = 'arn:aws:sns:us-east-1:144272576793:covid-19-etl-SNS'
    message = 'New Data insert into DynamoDB Table'
    sns.publish(TopicArn=topic_arn, Message=message)

    return {
        "message": "New Data insert into DynamoDB Table",
    }