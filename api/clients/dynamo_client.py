import boto3
import logging
from boto3.dynamodb.conditions import Key, Attr
from models.article import Article
from settings import DynamoConfig

class DynamoClient():
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(DynamoConfig.TABLE_NAME)

    def query_date(self, date):
        key_condition_expression = Key('date').eq(date)
        kwargs = {
            'KeyConditionExpression': key_condition_expression,
            'Limit': DynamoConfig.DYNAMODB_QUERY_LIMIT
        }
        response = self.table.query(**kwargs)
        try:
            new_article = Article(response['Items'])
            return new_article
        except:
            logging.error(f'DynamoClient error :: object returned from DB has no field "Items" {key_condition_expression} :: {response}')
        
    def query_date_range_for_articles(self, dates_to_query):
        response = [] 
        for query_date in dates_to_query:
            response.extend(self.query_date(query_date))
        return response
