# Paper: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0144296#authcontrib
# Another data source: https://www.frontiersin.org/articles/10.3389/fpsyg.2022.921388/full

import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://kt.ijs.si/data/Emoji_sentiment_ranking"
# Create object page
page = requests.get(url)

soup = BeautifulSoup(page.text)
table = soup.find("table", id="myTable")

# Obtain every title of columns with tag <th>
headers = []
for i in table.find_all("th"):
    title = i.text
    headers.append(title)

    # Create a dataframe
mydata = pd.DataFrame(columns=headers)
# Create a for loop to fill mydata
for j in table.find_all("tr")[1:]:
    row_data = j.find_all("td")
    row = [i.text for i in row_data]
    length = len(mydata)
    mydata.loc[length] = row

# Export dataframe to csv
mydata.to_csv(
    "../processed_data/text_analysis/emoji_sentiment_ranking.csv", index=False
)
