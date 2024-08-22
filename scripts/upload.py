import os
import sys

from kaggle.api.kaggle_api_extended import KaggleApi

def main(args):
    input_dir = args[0]
    
    api = KaggleApi()
    api.authenticate()
    
    event_dirs = [
        name for name in os.listdir(input_dir) 
        if os.path.isdir(os.path.join(input_dir, name))
    ]
    for event_dir in event_dirs:
        api.dataset_create_version(
            os.path.join(input_dir, event_dir),
            "Update"
        )

if __name__ == "__main__":
    main(sys.argv[1:])