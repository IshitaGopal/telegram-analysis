import re
import emoji
import nltk
import string


nltk.download("stopwords")
from nltk.corpus import stopwords

from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("russian")

STOPWORDS = stopwords.words("russian")


def clean_text(text):
    text = text.lower()
    text = remove_urls(text)
    text = remove_emojis(text)
    text = remove_punctuation(text)
    text = re.sub(r"\W+", " ", text)
    text = " ".join([word for word in text.split(" ") if word not in STOPWORDS])
    text = " ".join([stemmer.stem(word) for word in text.split(" ")])
    text = remove_white_spaces(text)
    return text


# stem russian text
def stem_text(text):
    return " ".join([stemmer.stem(word) for word in text.split(" ")])


# remove punctuation from string
def remove_punctuation(text):
    translator = str.maketrans("", "", string.punctuation)
    return text.translate(translator)


# function to remove urls from text
def remove_urls(text):
    url_pattern = re.compile(r"https?://\S+|www\.\S+")
    return url_pattern.sub(r"", text)


# remove extra white spaces from string
def remove_white_spaces(string):
    return re.sub(r"\s+", " ", string).strip()


# function to remove emojis from string
def remove_emojis(data):
    emoj = re.compile(
        "["
        "\U0001F600-\U0001F64F"  # emoticons
        "\U0001F300-\U0001F5FF"  # symbols & pictographs
        "\U0001F680-\U0001F6FF"  # transport & map symbols
        "\U0001F1E0-\U0001F1FF"  # flags (iOS)
        "\U00002500-\U00002BEF"  # chinese char
        "\U00002702-\U000027B0"
        "\U00002702-\U000027B0"
        "\U000024C2-\U0001F251"
        "\U0001f926-\U0001f937"
        "\U00010000-\U0010ffff"
        "\u2640-\u2642"
        "\u2600-\u2B55"
        "\u200d"
        "\u23cf"
        "\u23e9"
        "\u231a"
        "\ufe0f"  # dingbats
        "\u3030"
        "]+",
        re.UNICODE,
    )
    return re.sub(emoj, "", data)


# function to list the emojis in string
def Emoji_list(text):
    emoji_list = []
    for char in text:
        if char in emoji.EMOJI_DATA.keys():
            emoji_list.append(char)
    return emoji_list
