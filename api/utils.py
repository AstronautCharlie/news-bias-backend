from datetime import datetime, timedelta

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
    
def prune_empty_params(query_params):
    pruned_params = {} 
    for k, v in query_params.items():
        if v is not None and len(str(v)) > 0 and not str(v).isspace():
            pruned_params[k] = v
    return pruned_params