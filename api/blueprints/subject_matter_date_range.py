from flask import Blueprint, request, jsonify
from clients.dynamo_client import DynamoClient
from models.subject_model import SubjectModel
import logging
from datetime import datetime, timedelta 

article_search_bp = Blueprint('article_search', __name__)

@article_search_bp.route('/article_search', methods=['GET'])
def get_subject_matter_in_date_range(): 
    query_params = {
        'search_date': request.args.get('searchDate'),
        'start_date': request.args.get('startDate'),
        'end_date': request.args.get('endDate'),
        'subject_matter': request.args.get('subjectMatter')
    }
    try:
        validate_query_parameters(query_params)
    except Exception as err:
        logging.error(f'Query parameter validation failed with error :: {err}')

    articles = query_articles_into_subjects(query_params)
    
    return articles

def query_articles_into_subjects(query_params):

    dates_to_query = get_dates_from_parameters(query_params)
    client = DynamoClient()
    kwargs = {}
    for query_date in dates_to_query:
        logging.info(f'querying on date {query_date}')
        kwargs['subject_matter'] = query_params['subject_matter']
        kwargs['dates_to_articles'] = client.query_item(query_date)
    response = SubjectModel(**kwargs) 

    return response

def get_dates_from_parameters(query_params):
    if 'search_date' in query_params:
        return [query_params['search_date']]
    else:
        date_format = '%Y-%m-%d'
        start_date = datetime.strptime(query_params['start_date'], date_format)
        end_date = datetime.strptime(query_params['end_date'], date_format)

        date_range = [] 
        current_date = start_date 
        while current_date <= end_date: 
            date_range.append(current_date.strftime(date_format))
            current_date += timedelta(days=1)
        
        return date_range
    
def validate_query_parameters(query_params):
    date_format = '%Y-%m-%d'

    if 'subject_matter' not in query_params:
        raise ValueError('Parameter validation failed: \'subject matter\' is a required parameter')

    if 'search_date' in query_params:
        if ('start_date' in query_params or 'end_date' in query_params):
            raise ValueError('Parameter validation failed: should only have one of \'search_date\' and \'start_date\'/\'end_date\'')
        try:
            datetime.strptime(query_params['search_date'], date_format)
        except:
            raise ValueError(f'Parameter validation failed: search date ({query_params["search_date"]}) must be of the form "YYYY-MM-DD"')
    
    if ('start_date' in query_params and 'end_date' not in query_params) or ('start_date' not in query_params and 'end_date' in query_params):
        raise ValueError('Parameter validation failed: cannot have one of \'start_date\'/\'end_date\' without the other')
    
    if ('start_date' in query_params) and ('end_date' in query_params):
        if datetime.strptime(query_params['start_date'], '%Y-%m-%d') > datetime.striptime(query_params['end_date'], '%Y-%m-%d'): 
            raise ValueError(f'Parameter validation failed: start date ({query_params["start_date"]}) is later than end date ({query_params["end_date"]})')
        try:
            datetime.strptime(query_params['start_date'], date_format)
            datetime.strptime(query_params['end_date'], date_format)
        except:
            raise ValueError(f'Parameter validation failed: start/end dates ({query_params["start_date"]}/{query_params["end_date"]}) must be of the form "YYYY-MM-DD"')