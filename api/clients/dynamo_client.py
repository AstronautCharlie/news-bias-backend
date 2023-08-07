import boto3
import logging
from boto3.dynamodb.conditions import Key, Attr
from api.models.article import Article
from api.settings import DynamoConfig

class DynamoClient():
    def __init__(self):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(DynamoConfig.TABLE_NAME)

    def query_date(self, date, exclusive_start_key=None):
        logging.info(f'making key_condition_expression with date :: {date}')
        key_condition_expression = Key('date').eq(date)
        kwargs = {
            'KeyConditionExpression': key_condition_expression,
            'Limit': DynamoConfig.DYNAMODB_QUERY_LIMIT
        }
        if exclusive_start_key is not None:
           logging.info(f'setting ExclusiveStartKey to :: {exclusive_start_key}')
           kwargs['ExclusiveStartKey'] = exclusive_start_key
        logging.info(f'about to query db with KeyConditionExpression :: {kwargs["KeyConditionExpression"]}')
        
        response = self.table.query(**kwargs)
        try:
            articles_on_day = response['Items']
            new_articles = []
            for article in articles_on_day:
                new_article = Article(article)
                new_articles.append(new_article)
            return new_articles, response['LastEvaluatedKey']
        except:
            logging.error(f'DynamoClient error :: failed to convert DB response into Articles {key_condition_expression} :: {str(response)[:5000]} :: truncating response at 5000 characters')
        
    def query_date_range_for_articles(self, dates_to_query, exclusive_start_key=None):
        response = [] 
        logging.info(f'dates to query are :: {dates_to_query}')
        for query_date in dates_to_query:
            logging.info(f'querying date :: {query_date}')
            articles, last_evaluated_key = self.query_date(query_date, exclusive_start_key=exclusive_start_key)
            if articles is None:
                logging.info(f'no articles found on date {articles}')
            response.extend(articles)
        return response
