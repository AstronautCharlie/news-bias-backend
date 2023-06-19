# What is this? 
This repo defines the backend server for the News Bias project

# How do I run it?
Navigate to top level directory 

Run `python api`

# What's the last thing I did? 
Fetch stories in a date range and load them into SubjectModels

# What's next to do? 
Move code for fetching stories in date range into SubjectModels into a service - it shouldn't be its own endpoint. The endpoint should get embeddings of articles based on subject matter. 