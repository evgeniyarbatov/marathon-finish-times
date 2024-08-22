
import os
import sys

import pandas as pd

def main(args):
    input_dir = args[0]
    
    dfs = []
    
    event_dirs = [
        name for name in os.listdir(input_dir) 
        if os.path.isdir(os.path.join(input_dir, name))
    ]
    for event_dir in event_dirs:     
        for subdir, _, files in os.walk(
            os.path.join(input_dir, event_dir)
        ):
            for file in files:                
                if file != f'{event_dir}.csv':
                    continue
                
                file_path = os.path.join(subdir, file)
                
                df = pd.read_csv(file_path)
                
                df = df.sort_values(by='Rank', ascending=True)
                
                df.rename(columns={
                    'Mark': 'Time', 
                    'Competitor': 'Name',
                    'DOB': 'Date of Birth',
                    'Pos': 'Place',
                    'Nat': 'Country',
                    'Venue': 'City',
                }, inplace=True)
                
                df = df[[
                    'Rank',
                    'Time',
                    'Name',
                    'Country',
                    'Date of Birth',
                    'Place',
                    'City',
                    'Date',
                    'Gender',
                    'Event',
                ]]
                
                df['Name'] = df['Name'].str.title()
                
                for col in ['Date of Birth', 'Date']:
                    df[col] = pd.to_datetime(df[col], exact=False, dayfirst=True).dt.strftime('%d.%m.%Y')
                
                df['City'] = df['City'].str.replace(r'\s*\(.*\)|,.*', '', regex=True)
                
                df.to_csv(
                    f'{input_dir}/{event_dir}/{event_dir}.csv', 
                    index=False,
                )


if __name__ == "__main__":
    main(sys.argv[1:])