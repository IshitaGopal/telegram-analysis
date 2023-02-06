# TelegramProject

## Data collection from Telegram 
The code for this is in the chat_data_collection direcotry 

### Getting started
You will need to:
1. Download the Telegram app and create an account - this will require a phone number.
2. Get api_id, api_hash - to access Telegram's API

https://my.telegram.org/ -> https://my.telegram.org/apps


### Save API cridentials in a .env file 
You dont want to share the api keys with everyone. dotenv allows us to access private credentials from a secret file. This file has the name ".env". These files dont show up in the file browsers. 

1. 
```
pip install python-dotenv
```
2. create a file with name .env 
3. put your API key and hash in the following format

```
TELEGRAM_API_ID = "987298"
TELEGRAM_API_HASH = "o898dnjdu23801kmcloewij"
PHONE_NUM = "+19810023456"

```
###  Add the .env file to .gitignore file 
.gitignore allows us to list files which we want git to ignore. We want to ignore the .env file and not commit it to the Git repo. 

note: [gitignore.io](https://www.toptal.com/developers/gitignore/) is a nice resource for automatically generating .gitignore with files which are usually ignored/

### Using Telethon to access the API
1. [Telethon](https://docs.telethon.dev/en/stable/) is a Python library which is a wrapper for the Telegram API and makes it quite easy to interact with Telegram's API. I use the get_messages() method to collect messages which takes the channel/group id as an input. 

TelegramClient creates a client which makes requests on your behalf to the API in order and retrieves information (or changes something within the application) Avaialble (methods)[https://docs.telethon.dev/en/stable/quick-references/client-reference.html#messages] 

```
# Example 
with TelegramClient(session, api_id, api_hash) as client:
        messages = client.get_messages(channel_input, limit=100)

```

2. Public channels/group chats have a unique usernames similar to @username in Twitter. For example, the telegram channel of the NYT can be found here: https://telegram.me/@nytimes. nytimes is the unique userid we can use to fetch messages.

```
# Example 
channel_input = "nytimes"
with TelegramClient(session, api_id, api_hash) as client:
        messages = client.get_messages(channel_input, limit=100)

```
3. TelegramClient() creates session files - these files contain enough information for you to login without re-sending the code each time you make a request. 

Other advantages of session file: they also save "input entities" that you’ve "seen" so that you can get information about a user or channel just by their numeric Ids. "(chats and channels with their name and username, and users with the phone too) can be found in the session file, so that you can quickly access them."

note: An entity can be any User, Chat or Channel object that the API may return in response to certain methods.

For example, from the 100 messages we collected from nytimes, if there was a forwarded message, the API response will return an "numeric id" associated with the orignal channel/user/group(if its public!). You can use this id to get the username of the channel. Say its @bbcnews. We can then use API methods using bbcnews as the input. 

The session input requires us to provide the name of the session file. As explained in the docs, if we create a TelegramClient('anon') instance and connect, an anon.session file will be created in the working directory (In this case the inside code_for_data_collection/). We can also pass in absolute paths instead of strings. These files cache the access_hash associated with the entities’ ID


### Collect all the messages 
To collect all the messages from a public channel or a public group on Telegram:

1. execute collect_all_messages.py [script](https://github.com/IshitaGopal/TelegramProject_23/blob/code_for_data_collection/code/collect_all_messages.py) in the terminal. 
2. This will use code in Config.py and collect_all_messages.py files so make sure you have both of them.
2. You will need to provide a channel/group username as the input argument. 
3. The below example will collect all the messages from New York Time's telegram channel (viewable at t.me/nytimes) in json format. 

```console
foo@bar:~$ ./collect_all_messages.py nytimes
```

note: The first time, you will be prompted to input your phone number and autheticate by providing the code sent to you on Telegram app. 


4. Each json file will contain a maximum of 10000 messages and will be suffixed by the message id of the last post collected. 
5. There will be multiple json files if there are more than 10000 messages to collect.
6. The script creates a folder with the same name as the channel and stores all  json files in it. 
7. The chanel folder is stored within the "json_chat_data" (see config.py). E.g. path of a json file:

```
json_chat_data/nytimes/nytimes_1.json
```

8. note: You can change to the directory names/session file names if you want in the Config.py file 


The API Keys are stored as enviroment variables and are imported from config.py.

---
**NOTE**
 You will need your own API cridentials ([see here](https://docs.telethon.dev/en/stable/basic/signing-in.html))and add them to a .env file.  [This](https://www.youtube.com/watch?v=YdgIWTYQ69A) tutorial by Jonathan Soma shows how to do this. The format of the .env file should be as follows:

```
TELEGRAM_API_ID = ""
TELEGRAM_API_HASH = ""
PHONE_NUM = ""

```
---



 

