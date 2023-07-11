# What is this? 
This repo defines the backend server for the News Bias project

# How do I run it?
Navigate to top level directory. Set your openAI API key to the environment variable 'OPENAI_API_KEY'

Run `python api`

# What's the last thing I did? 
Embeddings are returned in JSON blob. 

# What's next to do? 
Make front end. Also experiment with how to make relevance screen better - it missed a few obvious cases where it didn't realize 'Joe Biden' and 'Biden' are the same person.
Clean up article text so we're not using quite so many tokens. 