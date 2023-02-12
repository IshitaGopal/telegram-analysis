import wikipedia
from nltk.tokenize import sent_tokenize
import pandas as pd
import os
from Config import Config
import secrets
from tqdm.auto import tqdm

# set language to russian
wikipedia.set_lang("ru")

# 5000 random topics
num_topics = 5000
random_topic = wikipedia.random(num_topics)

# Get the first 1000 sentences from each topic
sentences = []
for i in tqdm(range(num_topics)):
    topic = random_topic[i]
    try:
        get_1000_sentences = sent_tokenize(wikipedia.page(topic).content[:1000])
        sentences.append(secrets.choice(get_1000_sentences))
    except:
        pass

# Save to file
f_path = os.path.join(Config.proccessed_data_dir, "wiki_sentences.csv")
pd.DataFrame({"wiki_randomSent": sentences}).to_csv(f_path, index=False)
