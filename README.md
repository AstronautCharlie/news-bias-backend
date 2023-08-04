# What is this? 
This repo defines the backend server for the News Bias project

# How do I run it?
Navigate to top level directory. Set your openAI API key to the environment variable 'OPENAI_API_KEY'

Run `python api`

# What's the last thing I did? 
Topic coverage endpoint works, but needs pagination - right now it's pulling 50 at a time, and that takes too long. Add pagination with page size...25? 

# What's next to do? 
Implement pagination, then play around to see what trends I can discover. 

Honestly, probably fix the damn scrapers.

Add tokens consumed to logs

I added an Article class to store responses from DynamoDB, and subject_matter_embeddings hasn't been updated to reflect this change - it still expects articles to be dictionaries, so it's broken. Fix it. 

