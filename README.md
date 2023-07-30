# What is this? 
This repo defines the backend server for the News Bias project

# How do I run it?
Navigate to top level directory. Set your openAI API key to the environment variable 'OPENAI_API_KEY'

Run `python api`

# What's the last thing I did? 
Made first pass at topic coverage endpoint. Need to debug

# What's next to do? 
We're pivoting - start with simple topic coverage by headline analysis. For a given date range, track how much each news source covered a given topic, and pick out what the most common headline topics were. This will mean I have to go back and fix the scrapers.... but that had to happen eventually anyway. 

I added an Article class to store responses from DynamoDB, and subject_matter_embeddings hasn't been updated to reflect this change - it still expects articles to be dictionaries, so it's broken. Fix it. 

Add tokens consumed to logs

Debug `/topics`