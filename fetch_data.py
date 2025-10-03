import os
from dotenv import load_dotenv
from newsapi import NewsApiClient

load_dotenv()

API_KEY = os.getenv('API_KEY')
newsapi = NewsApiClient(API_KEY)

top_headlines = newsapi.get_top_headlines(q='bitcoin',
                                          category='business',
                                          language='en',
                                          country='us')

print(top_headlines)
