# What is this? 
This repo defines the backend server for the News Bias project

# How do I run it?
Navigate to top level directory. Set your openAI API key to the environment variable 'OPENAI_API_KEY'

Run `python api`

# What's the last thing I did? 
Topic coverage endpoint works, but needs pagination. Going to do server-side calculation. However, too many 
stories to get them all for each day (until I know this works better). Add a random sampler for now. Also
return tokens consumed from chat clients

# What's next to do? 
Implement pagination, with random sampler until I know this works. 

Add tokens consumed to chat client response

Honestly, probably fix the damn scrapers.

I added an Article class to store responses from DynamoDB, and subject_matter_embeddings hasn't been updated to reflect this change - it still expects articles to be dictionaries, so it's broken. Fix it. 

