from flask import Blueprint, request, jsonify
from clients.dynamo_client import DynamoClient
from clients.chat_client import ChatClient
from utils import prune_empty_params, get_dates_from_parameters
from response_schemas.topic_coverage import TopicCoverageResponse
import logging
from datetime import datetime, timedelta 
import json

topic_coverage_bp = Blueprint('topic_coverage', __name__)

@topic_coverage_bp.route('/topic_coverage', methods=['GET', 'POST'])
def topic_coverage():
    request_args = request.args
    query_params = {
        'search_date': request_args.get('searchDate'),
        'start_date': request_args.get('startDate'),
        'end_date': request_args.get('endDate'),
        'topic': request_args.get('topic'),
        'last_evaluted_key': request_args.get('lastEvaluatedKey')
    }
    logging.info(f'query params are :: {query_params}')
    query_dates = get_dates_from_parameters(query_params)
    logging.info(f'got query dates from get_dates_form_parameters :: {query_dates}')
    query_topic = query_params['topic']

    db_client = DynamoClient()
    chat_client = ChatClient()

    logging.info('querying db')
    articles = db_client.query_date_range_for_articles(query_dates, query_params['last_evaluted_key'])
    logging.info('tagging stories by relevance')
    articles = chat_client.tag_stories_by_relevance(articles, query_topic)

    # Calculate coverage 
    response = TopicCoverageResponse(articles, query_topic)
    response.calculate_coverage()

    final_response = response.build_json_response()
    logging.info(f'subject matter :: {response.topic}')
    logging.info(f'coverage :: {response.coverage}')
    for a in response.articles:
        logging.info(f'{a.article_headline} :: relevance? {a.relevance}')
    return final_response