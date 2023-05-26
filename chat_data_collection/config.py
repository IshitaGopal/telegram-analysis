import os
from dotenv import load_dotenv

# load enviroment variables from the .env file
load_dotenv()

#
class Config:
    api_id = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")
    phone = os.getenv("PHONE_NUM")
    session_name = "anon.session"

    json_for_analysis = "json_chat_analysis"
    json_channel_dir = "json_channel_data"
    processed_data_dir = "processed_data"
    chat_dfs_dir = "chat_dfs"
    chat_dfs_csv_dir = "chat_dfs_csv"
    fwds_master_file = "fwds_master.pkl"

    analysis_min_date = "2020-08-09"
    analysis_max_date = "2021-04-01"
