import sys
import requests
import os
import json
import pickle

import pandas as pd

from bs4 import BeautifulSoup

MAX_PAGE_COUNT = 100

def cache(filename):
    def decorator(func):
        def wrapped(*args):
            key = (args)
            try:
                hash(key)
            except TypeError as e:
                return func(*args)
            try:
                with open(filename, 'rb') as f:
                    cache = pickle.load(f)
            except Exception:
                cache = {}
            if key in cache:
                return cache[key]
            else:
                value = func(*args)
                if value is not None:
                    cache[key] = value
                    with open(filename, 'wb') as f:
                        pickle.dump(cache, f)
                    return value
        return wrapped
    return decorator

@cache('cache/scrape.pickle')
def get_url(url):
    print('Fetching', url)
    response = requests.get(url, verify=False)
    if response.status_code == 200:
        return response.content
    else:
        return None

def parse_html(content):
    soup = BeautifulSoup(content, 'html.parser')
    
    table = soup.find('table')
    if table is None:
        return None
    
    rows = []
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        cells = [cell.text.strip() for cell in cells]
        if len(cells) > 0:
            rows.append(cells)

    headers = [header.text.strip() for header in table.find_all('th')]

    return pd.DataFrame(rows, columns=headers)

def main(args):
    config_file = args[0]
    output_dir = args[1]

    os.makedirs(output_dir, exist_ok=True)

    with open(config_file, 'r') as file:
        configs = json.load(file)
        
    for config in configs:
        event = config['event']
        gender = config['gender']
        
        date = config['date']
        
        event_dir = f"{output_dir}/{event.lower()}/{gender.lower()}"
        os.makedirs(event_dir, exist_ok=True)

        for page_number in range(1, MAX_PAGE_COUNT):
            url = config['url']
            
            url = url.replace("TODAYS_DATE", f"{date}")
            url = url.replace("PAGE_NUMBER", f"{page_number}")

            content = get_url(url)
                        
            df = parse_html(content)
            if df is None:
                break
            
            df['Gender'] = gender
            df['Event'] = event
            
            df = df[[
                'Rank',
                'Mark',
                'Competitor',
                'Gender',
                'Event',
                'DOB',
                'Nat',
                'Pos',
                'Venue',
                'Date',
            ]]
            
            df.to_csv(f'{event_dir}/{page_number}.csv', index=False)

if __name__ == "__main__":
    main(sys.argv[1:])