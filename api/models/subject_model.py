class SubjectModel:
    def __init__(self, subject_matter, dates_to_articles=None):
        self.subject_matter = subject_matter
        self.dates_to_articles = dates_to_articles
    
    def __str__(self):
        response = f'Subject matter :: {self.subject_matter}'
        if self.dates_to_articles is not None:
            response += f'\n{[(date, str(articles)[:50]) for date, articles in self.dates_to_articles]}'
        return response