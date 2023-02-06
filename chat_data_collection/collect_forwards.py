import os
from config import Config, collect_fwds_info
import pandas as pd
import glob as glob
import time
import argparse
import logging


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--channel_input", type=str, required=True)
    args = parser.parse_args()

    start_time = time.time()

    # path of the pickled channel dataframe
    channel_pkl_path = os.path.join(
        Config.processed_data_dir, Config.chat_dfs_dir, args.channel_input + ".pkl"
    )
    print(channel_pkl_path)

    # channel dataframe
    channel_df = pd.read_pickle(channel_pkl_path)

    # path of the forwards master file
    fwds_master_path = os.path.join(Config.processed_data_dir, Config.fwds_master_file)

    # check if forwards master file exists else create one
    if os.path.exists(fwds_master_path) == False:
        fwd_cols = [
            "fwd_id",
            "fwd_username",
            "fwd_title",
            "fwd_user_created",
            "fwd_is_verified",
            "fwd_is_broadcast",
            "fwd_is_megagroup",
            "fwd_is_gigagroup",
        ]
        pd.DataFrame(columns=fwd_cols).to_pickle(fwds_master_path)

    # existing list of forwards ids
    fwds_master_df = pd.read_pickle(fwds_master_path)
    fwds_master_ids = fwds_master_df.fwd_id.dropna().astype(int).tolist()

    # get a list of unique forwrd ids in the input dataframe
    channel_fwd_ids = channel_df[channel_df.fwd_type == "PeerChannel"]["fwd_id"]
    channel_fwd_ids = channel_fwd_ids.drop_duplicates().astype(int).tolist()
    print(f"Total number of unique forwards found: {len(channel_fwd_ids)}")

    # Filter out forward ids which already exist in the master list
    new_fwd_ids = [value for value in channel_fwd_ids if value not in fwds_master_ids]
    print(f"Number of forwards to collect: {len(new_fwd_ids)}")

    # Collect information for the remaining ids using collect_fwds_info()
    # And update the forwrds master dataframe
    if len(new_fwd_ids) > 0:
        new_fwds_df = collect_fwds_info(new_fwd_ids)
        fwds_master_df = pd.concat([fwds_master_df, new_fwds_df])
        fwds_master_df.to_pickle(fwds_master_path)
        print("Updated forwards master file")

    # Merge in forwards info into the channel df
    channel_df = channel_df.merge(fwds_master_df, how="left", on="fwd_id")
    print("Merged forwards information")

    # Save the updated channel df
    channel_df.to_pickle(channel_pkl_path)
