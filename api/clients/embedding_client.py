import openai
import os
from settings import EmbeddingClientConfig
from tenacity import retry, wait_random_exponential, stop_after_attempt

class EmbeddingClient():
    def __init__(self):
        self.model_id = EmbeddingClientConfig.EMBEDDING_MODEL
        openai.api_key = os.environ.get('OPENAI_API_KEY')
    
    @retry(wait=wait_random_exponential(min=1, max=20), stop=stop_after_attempt(3))
    def get_embedding(self, input):
        response = openai.Embedding.create(
            input=input, model=self.model_id
        )
        embedding = response['data'][0]['embedding']

        return embedding