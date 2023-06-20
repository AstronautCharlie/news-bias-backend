import boto3
import logging
from boto3.dynamodb.conditions import Key, Attr
from settings import DynamoConfig

class DynamoClient():
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(DynamoConfig.TABLE_NAME)

    def query_item(self, date):
        key_condition_expression = Key('date').eq(date)
        kwargs = {
            'KeyConditionExpression': key_condition_expression,
            'Limit': DynamoConfig.DYNAMODB_QUERY_LIMIT
        }
        response = self.table.query(**kwargs)
        try:
            return response['Items']
        except:
            logging.error(f'DynamoClient error :: query failed with key {key_condition_expression} :: {response}')
        
    def query_dates(self, dates_to_query):
        response = {} 
        for query_date in dates_to_query:
            response[query_date] = self.query_item(query_date)
        return response
