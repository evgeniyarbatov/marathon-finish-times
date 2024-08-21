import sys
import requests
import shutil
import os

import pandas as pd

from bs4 import BeautifulSoup

def main(args):
    url = args[0]
    output_dir = args[1]

    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir, exist_ok=True)

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
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