import sys
import requests
import shutil
import os
import json
import pickle

import pandas as pd

from bs4 import BeautifulSoup

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
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        return None

def main(args):
    config_file = args[0]
    output_dir = args[1]

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    with open(config_file, 'r') as file:
        configs = json.load(file)
        
    for config in configs:
        url = config['url']

        content = get_url(url)
        soup = BeautifulSoup(content, 'html.parser')
        
        table = soup.find('table')
        headers = [header.text.strip() for header in table.find_all('th')]

        rows = []
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            cells = [cell.text.strip() for cell in cells]
            if len(cells) > 0:
                rows.append(cells)

        df = pd.DataFrame(rows, columns=headers)
        df.to_csv(f'{output_dir}/records.csv', index=False)

if __name__ == "__main__":
    main(sys.argv[1:])