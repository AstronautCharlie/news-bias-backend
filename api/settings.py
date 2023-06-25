class DynamoConfig:
    TABLE_NAME = 'raw_stories'
    DYNAMODB_QUERY_LIMIT = 10

class ChatClientConfig:
    DEFAULT_RELEVANCE_PROMPT = 'Is the article with the headline "{}" likely to be relevant to the subject of "{}"? Answer "yes" or "no"'
    CHAT_MODEL = 'gpt-3.5-turbo'

class EmbeddingClientConfig: 
    # At time of writing, test-embedding-ada-002 is the best practice to use 
    # for embeddings
    # https://platform.openai.com/docs/guides/embeddings/embedding-models
    EMBEDDING_MODEL = 'text-embedding-ada-002'