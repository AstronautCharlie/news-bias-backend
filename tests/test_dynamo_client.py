from unittest import TestCase
from unittest.mock import patch
from api.clients.dynamo_client import DynamoClient
import moto
import boto3

class TestDynamoClient(TestCase):

    @patch('api.clients.dynamo_client.DynamoClient.query_date')
    def test_query_item(self, mock_query):
        client = DynamoClient()

        mock_article = {
            'date': '2023-01-01',
            'article_headline': 'man bites dog',
            'article_text': 'just what it says on the tin',
            'source': 'fauxnews',
            'url': 'www.fauxnews.com/example',
            'link_headline': 'man bites dog'
        }
        mock_query.return_value = [mock_article]
        response = client.query_date('2023-03-01')
        assert response == [mock_article]
    
    @patch('api.clients.dynamo_client.DynamoClient.query_date')
    def test_query_dates(self, mock_query):
        client = DynamoClient()
        # Each value returned by query_item is expected to be a list
        mock_articles = [
            [{
                'date': '2023-01-01',
                'article_headline': 'man bites dog',
                'article_text': 'just what it says on the tin',
                'source': 'fauxnews',
                'url': 'www.fauxnews.com/example',
                'link_headline': 'man bites dog'
            }], [{
                'date': '2023-01-02',
                'article_headline': 'dog bites back',
                'article_text': 'just what it says on the tin',
                'source': 'fauxnews',
                'url': 'www.fauxnews.com/example',
                'link_headline': 'dog bites back'
            }]
        ]
        mock_query.side_effect = mock_articles
        response = client.query_date_range(['2023-01-01', '2023-01-02'])
        # Expected response is a list containing dictionaries representing articles
        assert response == [mock_articles[0][0], mock_articles[1][0]]
