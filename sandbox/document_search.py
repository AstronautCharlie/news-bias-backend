import boto3 

def search_date(story_date):
    client = boto3.client('dynamodb')
    table_name = 'raw_stories'

    response = client.query(
        TableName=table_name,
        KeyConditionExpression='#story_date=:story_date',
        ExpressionAttributeValues={':story_date': {'S': story_date}},
        ExpressionAttributeNames={'#story_date': 'date'}
    )

    return response