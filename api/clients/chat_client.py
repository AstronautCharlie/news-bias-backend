import openai
from settings import ChatClientConfig
import os
import logging

class ChatClient():
    def __init__(self):
        self.relevance_prompt = ChatClientConfig.DEFAULT_RELEVANCE_PROMPT
        self.model = ChatClientConfig.CHAT_MODEL
        openai.api_key = os.environ.get('OPENAI_API_KEY')

    def is_headline_relevant_to_subject_matter(self, headline, subject_matter):
        prompt = self.create_chat_prompt(headline, subject_matter)
        response_object = openai.ChatCompletion.create(model=self.model, messages=[{'role': 'user', 'content': prompt}])
        response_message = response_object['choices'][0]['message']['content']
        return response_message

    def create_chat_prompt(self, headline, subject_matter):
        return self.relevance_prompt.format(headline, subject_matter)