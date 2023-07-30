"""
Defines a response object for the `/topic_coverage` endpoint. Idea is that it provides
date-by-date records of coverage for the given topic
"""
import json

class TopicCoverageResponse:
    def __init__(self, articles, topic):
        self.articles = articles
        self.topic = topic 
        self.coverage = None

    def calculate_coverage(self):
        relevant_articles = [a for a in self.articles if a.is_relevant()]
        irrelevant_articles = [a for a in self.articles if a.is_irrelevant()]
        ambiguous_articles = [a for a in self.articles if a.is_ambiguously_relevant()]
        self.coverage = len(relevant_articles) / len(irrelevant_articles)

    def build_response(self):
        return json.dumps(self, default=lambda o: o.__dict__)
        