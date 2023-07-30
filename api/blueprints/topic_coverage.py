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
    logging.info(f'request is :: {request}')
    logging.info(f'{request.args}')
    #request_args = request.get_json()
    request_args = request.args
    logging.info(f'request args are :: {request_args}')
    query_params = {
        'search_date': request_args.get('searchDate'),
        'start_date': request_args.get('startDate'),
        'end_date': request_args.get('endDate'),
        'topic': request_args.get('topic')
    }
    query_params = prune_empty_params(query_params)
    query_dates = get_dates_from_parameters(query_params)
    query_topic = query_params['topic']

    logging.info(f'making clients')
    db_client = DynamoClient()
    chat_client = ChatClient()

    logging.info('querying db')
    articles = db_client.query_date_range(query_dates)
    articles = chat_client.tag_stories_by_relevance(articles, query_topic)

    logging.info('creating response')
    # Calculate coverage 
    response = TopicCoverageResponse(articles, query_topic)
    response.calculate_coverage()

    final_response = response.build_response()
    logging.info(f'subject matter :: {final_response.topic}')
    logging.info(f'coverage :: {final_response.coverage}')
    for a in final_response.articles:
        logging.info(f'{a.article_headline} :: relevance? {a.relevance}')
    return response.build_response()