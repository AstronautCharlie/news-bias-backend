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
            articles_on_day = response['Items']
            new_articles = []
            for article in articles_on_day:
                new_article = Article(article)
                new_articles.append(new_article)
            return new_articles
        except:
            logging.error(f'DynamoClient error :: failed to convert DB response into Articles {key_condition_expression} :: {str(response)[:5000]} :: truncating response at 5000 characters')
        
    def query_date_range_for_articles(self, dates_to_query):
        response = [] 
        for query_date in dates_to_query:
            articles_on_date = self.query_date(query_date)
            if articles_on_date is None:
                logging.info(f'no articles found on date {query_date}')
            response.extend(self.query_date(query_date))
        return response
