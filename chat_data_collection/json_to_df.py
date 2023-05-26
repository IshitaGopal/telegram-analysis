#!/usr/bin/env python3

import os
import pandas as pd
import glob as glob
import time
import argparse
from pathlib import Path

from config import Config
from data_utils import get_cleaned_dataframe


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel_input", type=str, required=True)
    args = parser.parse_args()
    # logging.basicConfig(level=logging.DEBUG)

    start_time = time.time()
    channel_input = args.channel_input

    Path(os.path.join(Config.processed_data_dir, Config.chat_dfs_csv_dir)).mkdir(
        parents=True, exist_ok=True
    )

    # get all the paths of all the json files associated with a channel
    json_pattern = os.path.join(Config.json_for_analysis, channel_input, "*.json")
    json_files = glob.glob(json_pattern)

    # read all jsona and convert into a single dataframe
    # keep only relevant fields/columns

    cols = [
        "id",
        "date",
        "message",
        "from_id",
        "fwd_from",
        "reply_to",
        "media",
        "entities",
        "views",
        "forwards",
        "edit_date",
        # "ttl_period",
    ]

    print(json_files)

    clean_dfs = pd.concat(
        [get_cleaned_dataframe(pd.read_json(f)[cols]) for f in json_files],
        ignore_index=True,
    )

    # add chat name
    clean_dfs["chat_name"] = channel_input

    print(clean_dfs)

    # save the cleaned dataframe
    # format: channel_input.csv
    csv_name = channel_input + ".csv"
    clean_dfs.to_csv(
        os.path.join(Config.processed_data_dir, Config.chat_dfs_csv_dir, csv_name),
        index=False,
    )
