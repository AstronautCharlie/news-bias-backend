"""
This class defines a the response schema for returning subject matter embeddings
"""
import json

class SubjectMatterResponse:
    def __init__(self, articles=None, subject_matter=None):
        self.articles=articles
        self.subject_matter=subject_matter

    def clean_headlines(self):
        for article in self.articles:
            article['article_headline'] = article['article_headline'].strip()

    def get_relevant_articles(self):
        response = [] 
        for article in self.articles:
            if 'is_relevant' in article.keys() and article['is_relevant'].lower() == 'yes':
                response.append(article)
        return response

    def get_irrelevant_articles(self):
        response = [] 
        for article in self.articles:
            if 'is_relevant' in article.keys() and article['is_relevant'].lower() == 'no':
                response.append(article)
        return response
    
    def get_ambiguously_relevant_articles(self):
        response = [] 
        for article in self.articles:
            if 'is_relevant' in article.keys() and article['is_relevant'].lower() not in ['yes', 'no']:
                response.append(article)
        return response

    def get_uncategorized_articles(self):
        response = []
        for article in self.articles:
            if 'is_relevant' not in article.keys():
                response.append(article)
        return response

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True)