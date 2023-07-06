# What is this? 
This repo defines the backend server for the News Bias project

# How do I run it?
Navigate to top level directory. Set your openAI API key to the environment variable 'OPENAI_API_KEY'

Run `python api`

# What's the last thing I did? 
Tests for dynamo client (turned out to be kind of irrelevant)
Got `/article_search` to the point where it should query on relevance except that the flask app isn't reading in the environment variable of the openAI API key yet.

# What's next to do? 
Get the flask app to recognize the openAI API key environment variable. Maybe get the UWSGI server going since I have to do that eventually?