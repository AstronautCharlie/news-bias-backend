from flask import Blueprint, request, jsonify
from clients.dynamo_client import DynamoClient
from clients.chat_client import ChatClient
from clients.embedding_client import EmbeddingClient
from response_schemas.subject_matter_embeddings import SubjectMatterResponse
import logging
from utils import get_dates_from_parameters, prune_empty_params
import json

article_search_bp = Blueprint('article_search', __name__)

@article_search_bp.route('/article_search', methods=['GET', 'POST'])
def get_subject_matter_in_date_range(): 
    logging.info(f'{request.get_json()}')
    request_args = request.get_json()

    query_params = {
        'search_date': request_args.get('searchDate'),
        'start_date': request_args.get('startDate'),
        'end_date': request_args.get('endDate'),
        'subject_matter': request_args.get('subjectMatter')
    }
    query_params = prune_empty_params(query_params)
    logging.info(f'parameters are {query_params}')

    query_dates = get_dates_from_parameters(query_params)

    client = DynamoClient()
    articles = client.query_date_range(query_dates)
    response = SubjectMatterResponse(articles=articles, subject_matter=query_params['subject_matter'])
    response.clean_headlines()

    tag_articles_by_headline_relevance(response)
    log_articles_by_relevance(response)
    get_relevant_article_embeddings(response)
    remove_irrelevant_articles(response)

    json_response = json.loads(response.toJSON())
    logging.info(f'response keys top level :: {json_response.keys()}')
    first_article = None
    for article in json_response['articles']:
        if article['is_relevant'] == 'Yes':
            first_article = article
            break
    if first_article is not None:
        for k, v in first_article.items():
            logging.info(f'key: {k} :: value: {str(v)[:1000]}')

    return jsonify(response.toJSON())
    
# def validate_query_parameters(query_params):
#     date_format = '%Y-%m-%d'

#     if 'subject_matter' not in query_params:
#         raise ValueError('Parameter validation failed: \'subject matter\' is a required parameter')

#     if 'search_date' in query_params:
#         if ('start_date' in query_params or 'end_date' in query_params):
#             raise ValueError('Parameter validation failed: should only have one of \'search_date\' and \'start_date\'/\'end_date\'')
#         try:
#             datetime.strptime(query_params['search_date'], date_format)
#         except:
#             raise ValueError(f'Parameter validation failed: search date ({query_params["search_date"]}) must be of the form "YYYY-MM-DD"')
    
#     if ('start_date' in query_params and 'end_date' not in query_params) or ('start_date' not in query_params and 'end_date' in query_params):
#         raise ValueError('Parameter validation failed: cannot have one of \'start_date\'/\'end_date\' without the other')
    
#     if ('start_date' in query_params) and ('end_date' in query_params):
#         if datetime.strptime(query_params['start_date'], '%Y-%m-%d') > datetime.striptime(query_params['end_date'], '%Y-%m-%d'): 
#             raise ValueError(f'Parameter validation failed: start date ({query_params["start_date"]}) is later than end date ({query_params["end_date"]})')
#         try:
#             datetime.strptime(query_params['start_date'], date_format)
#             datetime.strptime(query_params['end_date'], date_format)
#         except:
#             raise ValueError(f'Parameter validation failed: start/end dates ({query_params["start_date"]}/{query_params["end_date"]}) must be of the form "YYYY-MM-DD"')

def tag_articles_by_headline_relevance(response):
    client = ChatClient()
    for article in response.articles:
        article['is_relevant'] = client.is_headline_relevant_to_subject_matter(article['article_headline'], response.subject_matter)        

def log_articles_by_relevance(response): 
    logging.info('Relevant articles:')
    relevant_articles = response.get_relevant_articles()
    logging.info([article['article_headline'] for article in relevant_articles])

    logging.info('Irrelevant articles:')
    irrelevant_articles = response.get_irrelevant_articles()
    logging.info([article['article_headline'] for article in irrelevant_articles])

    logging.info('Articles of ambiguous relevance')
    ambiguous_articles = response.get_ambiguously_relevant_articles()
    logging.info([article['article_headline'] for article in ambiguous_articles])

def get_relevant_article_embeddings(response):
    client = EmbeddingClient()
    relevant_articles = response.get_relevant_articles()
    for article in relevant_articles:
        article_embedding = client.get_embedding(article['article_text'])
        article['embedding'] = article_embedding 

def remove_irrelevant_articles(response):
    articles_to_keep = [] 
    for article in response.articles:
        if article['is_relevant'] == 'Yes':
            articles_to_keep.append(article)
    response.articles = articles_to_keep