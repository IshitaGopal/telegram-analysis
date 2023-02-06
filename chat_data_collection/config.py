import os
import json
import pandas as pd
import re
from telethon.sync import TelegramClient
from telethon import errors
from dotenv import load_dotenv

# load enviroment variables from the .env file
load_dotenv()

#
class Config:
    api_id = os.getenv("TELEGRAM_API_ID")
    api_hash = os.getenv("TELEGRAM_API_HASH")
    phone = os.getenv("PHONE_NUM")
    session_name = "anon.session"

    json_chat_dir = "json_chat_data"
    processed_data_dir = "processed_data"
    chat_dfs_dir = "chat_dfs"
    fwds_master_file = "fwds_master.pkl"


# write to json
def write_json(data, output_dir, output_subdir, output_file):
    output_path = os.path.join(output_dir, output_subdir, output_file)
    print(output_path)
    with open(output_path, "w") as f:
        json.dump(data, f, default=str, ensure_ascii=False)


# clean collected json
def get_cleaned_dataframe(df):
    """takes in a dataframe as input and
    returns a dataframe with defined fields"""

    # Add indictors for nans
    df["has_from_id"] = df.from_id.notna()
    df["is_fwd"] = df.fwd_from.notna()
    df["is_reply"] = df.reply_to.notna()
    df["is_media"] = df.media.notna()
    df["has_entity"] = df.entities.notna()
    # size of lists
    n = df.shape[0]

    from_user_id = [None] * n
    media_type = [None] * n
    fwd_type = [None] * n
    fwd_id = [None] * n
    reply_to_msg_id = [None] * n
    msg_textUrls = [None] * n

    # Iterate throught the df and extract relevent information
    for index, row in df.iterrows():

        # Extract from id
        if row["has_from_id"] == True:
            from_user_id[index] = list(row["from_id"].values())[1]

        # Extract media type: Photo/Document/ ...
        if row["is_media"] == True:
            media_type[index] = re.sub("MessageMedia", "", row["media"]["_"])

        # Extract forward type and id
        if row["is_fwd"] == True:
            if row["fwd_from"]["from_id"] is not None:
                fwd_type[index], fwd_id[index] = list(
                    row["fwd_from"]["from_id"].values()
                )

        # Extract reply to msg id
        if row["is_reply"] == True:
            reply_to_msg_id[index] = row["reply_to"]["reply_to_msg_id"]

        # Extract text hyperlinks
        urls = []
        if row["has_entity"] == True and len(row["entities"]) > 0:
            for entry in row["entities"]:
                if entry["_"] == "MessageEntityTextUrl":
                    urls.append(entry["url"])
        msg_textUrls[index] = urls

    # Add collected info to the dataframe
    df["from_user_id"] = from_user_id
    df["media_type"] = media_type
    df["fwd_type"] = fwd_type
    df["fwd_id"] = fwd_id
    df["reply_to_msg_id"] = reply_to_msg_id
    df["msg_textUrls"] = msg_textUrls

    # return the updated dataframe
    return df


def collect_fwds_info(ids):
    """Takes a list of channel ids and
    returns a dataframe with below defined columns"""

    n = len(ids)
    fwd_id = [None] * n
    fwd_username = [None] * n
    fwd_title = [None] * n
    fwd_user_created = [None] * n
    fwd_is_verified = [None] * n
    fwd_is_broadcast = [None] * n
    fwd_is_megagroup = [None] * n
    fwd_is_gigagroup = [None] * n

    for index, value in enumerate(ids):
        try:
            with TelegramClient(
                Config.session_name, Config.api_id, Config.api_hash
            ) as client:

                entity = client.get_entity(value)
                print(entity.username, entity.id)
                fwd_id[index] = entity.id
                fwd_username[index] = entity.username
                fwd_title[index] = entity.title
                fwd_user_created[index] = entity.date
                fwd_is_verified[index] = entity.verified
                fwd_is_broadcast[index] = entity.broadcast
                fwd_is_megagroup[index] = entity.megagroup
                fwd_is_gigagroup[index] = entity.gigagroup

        except (
            errors.rpcerrorlist.ChannelPrivateError,
            ValueError,
        ) as e:  # Not in database.
            print(e)
            fwd_id[index] = value

        # if index % 100 == 0:
        #     print("sleeping for 200")
        #     time.sleep(200)

    new_fwds_dict = {
        "fwd_id": fwd_id,
        "fwd_username": fwd_username,
        "fwd_title": fwd_title,
        "fwd_user_created": fwd_user_created,
        "fwd_is_verified": fwd_is_verified,
        "fwd_is_broadcast": fwd_is_broadcast,
        "fwd_is_megagroup": fwd_is_megagroup,
        "fwd_is_gigagroup": fwd_is_gigagroup,
    }

    new_fwds_df = pd.DataFrame(new_fwds_dict)

    return new_fwds_df
