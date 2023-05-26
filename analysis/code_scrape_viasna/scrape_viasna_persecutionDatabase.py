#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests
from bs4 import BeautifulSoup
from tqdm.auto import tqdm


headers = [
    "No",
    "date_of_incident",
    "name",
    "gender",
    "article",
    "court_date",
    "judge",
    "court",
    "arrest",
    "penalty",
    "additionally",
]

min_date = "2020-08-01"
max_date = "2021-08-01"
max_page = 1226
list_of_lists = []


for i in tqdm(range(1, max_page + 1)):

    url = f"https://spring96.org/persecution?DateFrom={min_date}&DateTo={max_date}&page={i}"
    page = requests.get(url)  # Get response
    status_code = page.status_code  # should get status 200

    # page status is not 200 break the loop
    if status_code != 200:
        break

    # get data from page
    soup = BeautifulSoup(page.text, "html.parser")
    table = soup.find("table", {"class": "table table-bordered"})

    # Create a for loop to fill list_of_lists
    for j in table.find_all("tr")[1:]:
        row_data = j.find_all("td")
        row = [q.text for q in row_data]
        list_of_lists.append(row)

# Create dataframe
df = pd.DataFrame(list_of_lists, columns=headers)

# save dataframe
df.to_csv("processed_data/viasna_data/persecutionDatabase.csv", index=False)
