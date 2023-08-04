"""
Defines a response object for the `/topic_coverage` endpoint. Idea is that it provides
date-by-date records of coverage for the given topic
"""
import json
import logging
from settings import BaseConfig as Config

class TopicCoverageResponse:
    def __init__(self, articles, topic):
        self.articles = articles
        self.topic = topic 

    def calculate_coverage(self):
        relevant_articles = [a for a in self.articles if a.is_relevant()]
        irrelevant_articles = [a for a in self.articles if a.is_irrelevant()]
        ambiguous_articles = [a for a in self.articles if a.is_ambiguously_relevant()]

        coverage = {} 
        for source in Config.SOURCES:
            source_relevant_count, source_total_count = self._calculate_source_specific_coverage(source=source, articles=self.articles)
            if source_total_count == 0: 
                logging.info(f'no articles found for source :: {source}')
                ratio = 0
            else: 
                ratio = source_relevant_count / source_total_count
            coverage[source] = {'relevant_count': source_relevant_count, 
                                'total_count': source_total_count, 
                                'ratio': ratio}
        total_count = 0 
        relevant_count = 0 
        for s in Config.SOURCES:
            total_count += coverage[s]['total_count']
            relevant_count += coverage[s]['relevant_count']
        total_coverage = {'total_count': total_count, 
                          'relevant_count': relevant_count,
                          'coverage': relevant_count / total_count}
        coverage['total_coverage'] = relevant_count/total_count

        self.coverage = coverage

    def build_json_response(self):
        article_stubs = self._prune_articles_for_response()
        response = {}
        response['articles'] = article_stubs
        response['subject_matter'] = self.topic
        response['coverage'] = self.coverage
        return response
    
    def _calculate_source_specific_coverage(self, *, source, articles):
        source_count = 0
        relevant_count = 0 
        
        for a in articles:
            if a.source == source:
                source_count += 1
                if a.is_relevant(): 
                    relevant_count += 1 
        
        return relevant_count, source_count 
    
    def _prune_articles_for_response(self):
        """
        We don't want to return the full body of articles as an HTTP response. 
        Remove data we don't want returned including: 
            - full text of all articles
            - all irrelevant articles
        """
        article_stubs = []
        for a in self.articles:
            if not a.is_relevant():
                continue
            stub = a.__dict__
            logging.info(f'stub is :: {stub}')
            del stub['article_text']
            article_stubs.append(stub)
        return article_stubs
        