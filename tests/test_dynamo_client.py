from unittest import TestCase
from unittest.mock import patch
from api.clients.dynamo_client import DynamoClient
import moto
import boto3

class TestDynamoClient(TestCase):

    @patch('boto3.resources.base.ServiceResource.Table.query')
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
        mock_query.return_value = {'Items': [mock_article]}
        response = client.query_item('2023-03-01')
        assert response == [mock_article]