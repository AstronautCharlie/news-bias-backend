from datetime import datetime, timedelta
import logging

def get_dates_from_parameters(query_params):
    if 'search_date' in query_params and query_params['search_date'] is not None:
        return [query_params['search_date']]
    else:
        if 'start_date' not in query_params or query_params['start_date'] is None:
            raise ValueError('missing both start_date and search_date in query params - one is required')
        date_format = '%Y-%m-%d'
        start_date = datetime.strptime(query_params['start_date'], date_format)
        end_date = datetime.strptime(query_params['end_date'], date_format)

        logging.info(f'in utils')
        date_range = [] 
        current_date = start_date 
        logging.info(f'start date :: {start_date}')
        logging.info(f'end_date :: {end_date}')
        while current_date <= end_date: 
            logging.info(f'adding current date {current_date}')
            date_range.append(current_date.strftime(date_format))
            current_date += timedelta(days=1)
        
        return date_range
    
def prune_empty_params(query_params):
    pruned_params = {} 
    for k, v in query_params.items():
        if v is not None and len(str(v)) > 0 and not str(v).isspace():
            pruned_params[k] = v
    return pruned_params