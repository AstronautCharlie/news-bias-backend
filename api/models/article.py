"""
Defines an Article as received from DynamoDB
"""

class Article:
    def __init__(self, article_dict):
        expected_keys = ['date', 
                           'url', 
                           'article_text', 
                           'article_headline', 
                           'link_headline', 
                           'source', 
                           'relevance']

        for key in expected_keys:
            setattr(self, key, article_dict.get(key))
    
    def set_relevance(self, relevance_response):
        self.relevance = relevance_response
    
    def is_relevant(self):
        return self.relevance.lower() == 'yes'

    def is_irrelevant(self):
        return self.relevance.lower() == 'no'
    
    def is_ambiguously_relevant(self):
        return self.relevance.lower() not in ['yes', 'no']
    
    def get_property(self, property_name):
        return getattr(self, property_name)