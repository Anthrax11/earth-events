"""Extracting the raw data"""
import requests
import json
import os

from src.config import read_config
from src.utils import get_absolute_path, get_timestamp, get_date


def make_request(url: str) -> dict:
    resp = requests.get(url)
    return resp.json()

def save_data(data: str, path: str, *args) -> str:
    file_path = get_absolute_path(path, *args)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        f.write(data)
        
    print(f"Data saved as: {file_path}")

    return file_path
        
def read_from_api(task_instance=None):
    config = read_config()
    endpoint = config["endpoint"]
    raw_location = config["locations"]["raw"]

    data = make_request(endpoint)
    saved_at = save_data(
        json.dumps(data, indent=4), raw_location, get_date(), f"{get_timestamp()}.json"
        )

    if task_instance:
        task_instance.xcom_push(key="raw_data", value=saved_at)

def main():
    read_from_api()

if __name__ == "__main__":    
    main()