import os
import pandas as pd
from dotenv import load_dotenv
from newsapi import NewsApiClient

def api_runner():

    load_dotenv()

    API_KEY = os.getenv('API_KEY')
    newsapi = NewsApiClient(API_KEY)

    top_headlines = newsapi.get_top_headlines(category='business',
                                              language='en',
                                              country='us')


    df2 = pd.json_normalize(top_headlines, record_path=['articles'])
    df2['timestamp'] = pd.to_datetime('now')
    df = df2._append(df2)
    print(df)
    
    
api_runner()


