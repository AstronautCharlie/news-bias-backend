from flask import Blueprint, request, jsonify
from clients.dynamo_client import DynamoClient
import logging

article_search_bp = Blueprint('article_search', __name__)

@article_search_bp.route('/article_search', methods=['GET'])
def get_subject_matter_in_date_range(): 
    query_params = {
        'start_date': request.args.get('start_date'),
        'end_date': request.args.get('end_date'),
        'subject_matter': request.args.get('subject_matter')
    }

    client = DynamoClient()

    return client.query_item(query_params['start_date'])

    