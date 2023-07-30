import openai
from settings import ChatClientConfig
import os
import logging

class ChatClient():
    def __init__(self):
        self.relevance_prompt = ChatClientConfig.DEFAULT_RELEVANCE_PROMPT
        self.llm = ChatClientConfig.CHAT_MODEL
        openai.api_key = os.environ.get('OPENAI_API_KEY')

    def is_text_relevant_to_subject_matter(self, text, subject_matter):
        prompt = self.create_chat_prompt(text, subject_matter)
        response_object = openai.ChatCompletion.create(model=self.llm, messages=[{'role': 'user', 'content': prompt}])
        response_message = response_object['choices'][0]['message']['content']
        return response_message
    
    def tag_stories_by_relevance(self, articles, subject_matter, text_header='article_headline'):
        """
        Assuming `articles` is a list of dicts, assign relevance
        based on the 'headline'
        """
        for article in articles:
            text_to_scan = article[text_header]
            relevance_response = self.is_text_relevant_to_subject_matter(text_to_scan, subject_matter)
            article.set_relevance(relevance_response)
        return articles

    def create_chat_prompt(self, headline, subject_matter):
        return self.relevance_prompt.format(headline, subject_matter)