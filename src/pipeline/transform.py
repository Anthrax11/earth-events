"""Transforming the raw data into tabular"""
import json
import glob
import os

import pandas as pd

from src.config import read_config
from src.utils import get_absolute_path


def find_latest_directory(directory: str) -> str:
    if os.path.isdir(directory):
        latest_dir = max(
            os.path.join(directory, name)
                for name in os.listdir(directory)
                    if os.path.isdir(os.path.join(directory, name)
                                     )
                                     )
        return latest_dir

def find_latest_file(directory: str, pattern: str = "*") -> str:
    if os.path.isdir(directory):
        files = glob.glob(os.path.join(directory, pattern))
        return max(files)
    
def read_json(path: str) -> dict:
    with open(path, "r") as f:
        data = json.loads(f.read())
    return data

def write_df(df: pd.DataFrame, absolute_path: str) -> str:
    os.makedirs(os.path.dirname(absolute_path), exist_ok=True)
    df.to_csv(absolute_path, mode="w")
    print(f"Data saved as: {absolute_path}")

    return absolute_path

def transform(task_instance=None):
    config = read_config()
    raw_location = config["locations"]["raw"]
    norm_location = config["locations"]["normalized"]

    if task_instance:
        raw_output_path = task_instance.xcom_pull(key="raw_data", task_ids="read_from_api")
    else:
        output_directory = get_absolute_path(raw_location)
        latest_directory = find_latest_directory(output_directory)
        raw_output_path = find_latest_file(latest_directory)

    data = read_json(raw_output_path)

    # for consistency of the flow, the timestamp is taken from
    # the output path rather than by invoking datetime.now() again
    # which might result in the date to be different from the previous step
    raw_path_no_ext = os.path.splitext(raw_output_path)[0]
    date_directory, file_name = raw_path_no_ext.split(os.path.sep)[-2:]
    file_time = file_name.split("-")[1]

    dimension_columns = ['categories', 'sources', 'geometry']

    # writing the event table discarting the dimensions which will be written after
    events_df = pd.json_normalize(data["events"]).drop(columns=dimension_columns)
    events_path = get_absolute_path(norm_location, date_directory, file_time, "events.csv")
    write_df(events_df, events_path)

    # writing the dimensions
    for column in dimension_columns:
        df = pd.json_normalize(data['events'], record_path=column, meta=['id'], record_prefix=f'{column[3:]}_')
        path = get_absolute_path(norm_location, date_directory, file_time, f"{column}.csv")
        write_df(df, path)


def main():
    transform()

if __name__ == "__main__":
    main()
