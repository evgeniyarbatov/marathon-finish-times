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
                if (
                    file == f'{event_dir}.csv'
                    or not file.endswith('.csv')
                ):
                    continue
                
                file_path = os.path.join(subdir, file)
                df = pd.read_csv(file_path)
                dfs.append(df)

        all_dfs = pd.concat(dfs, ignore_index=True)
        
        all_dfs.to_csv(
            f'{input_dir}/{event_dir}/{event_dir}.csv', 
            index=False,
        )

if __name__ == "__main__":
    main(sys.argv[1:])