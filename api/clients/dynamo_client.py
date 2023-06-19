import boto3
import logging
from boto3.dynamodb.conditions import Key, Attr
from settings import DynamoConfig

class DynamoClient():
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(DynamoConfig.TABLE_NAME)

    def query_item(self, date, limit=10):
        key_condition_expression = Key('date').eq(date)
        kwargs = {
            'KeyConditionExpression': key_condition_expression,
            'Limit': limit
        }
        response = self.table.query(**kwargs)
        try:
            return response['Items']
        except:
            logging.error
        