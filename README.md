# TelegramProject

# Tutorials / Notebooks / Code

## Data collection from Telegram 
The code for this is in the chat_data_collection direcotry 

### Getting started
You will need to:
1. Download the Telegram app and create an account - this will require a phone number.
2. Get api_id, api_hash - to access Telegram's API

## Save Cridentials in a .env file 
You dont want to share the api keys with everyone. dotenv allows us to access private credentials from a secret file. These files dont show up in the file browsers. 

1. pip install python-dotenv
2. create a file with name .env 
3. put your API key and hash in the following format

```
TELEGRAM_API_ID = "987298"
TELEGRAM_API_HASH = "o898dnjdu23801kmcloewij"
PHONE_NUM = "+19810023456"

```


### Collect all the messages 
To collect all the messages from a public channel/group on Telegram, execute [this Python script](https://github.com/IshitaGopal/TelegramProject/blob/code_for_data_collection/code/collect_all_messages.py) in the terminal. You will need to provide a channel/group username as the input. The below example will collect all the messages from New York Time's telegram channel (viewable at t.me/nytimes) in json format. Each json file will contain a maximum of 10000 messages and will be suffixed by the message id of the last post collected. There will be multiple json files if there are more than 10000 messages to collect.
     
```console
foo@bar:~$ ./collect_all_messages.py nytimes
```
You will be prompted to input your phone number and autheticate by providing the code sent to you on Telegram. 

The script first creates a folder with the same name as the channel and stores all  json files in it. The chanel folder is stored in the "chat_data" root directory (see config.py). E.g. path of a json file:
 
 ```
chat_data/nytimes/nytimes_1.json
```

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



 

