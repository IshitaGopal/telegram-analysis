#!/usr/bin/env python
# coding: utf-8

# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd

# https://medium.com/dfrlab/pro-lukashenka-telegram-channels-amplify-disinformation-2f3b0cf0a140


# URL object
url = "https://prisoners.spring96.org/en/table"
page = requests.get(url)  # Get response
print(page.status_code)  # should get status 200

# get data from page
soup = BeautifulSoup(page.text, "html.parser")
table = soup.find("table", id="table")


# get all table rows
for prisoner_data in table.find_all("tbody"):
    rows = prisoner_data.find_all("tr")


# Loop over rows and collect columns
name = []
date_of_birth = []
gender = []
date_of_detention = []
charges = []
prison = []
prison_address = []
status = []

for row in rows:
    # prisoner name
    name.append(row.find_all("td")[0].text)
    # dob
    date_of_birth.append(row.find_all("td")[1].text)
    # gender
    gender.append(row.find_all("td")[2].text)
    # date of detention
    date_of_detention.append(row.find_all("td")[3].text)
    # charges
    charges.append(row.find_all("td")[4].text)
    # which prison number
    prison.append(row.find_all("td")[5].text)
    # prinson address
    n = row.find_all("td")[5].find("span")
    if n is not None:
        if n.has_key("data-address"):
            if len(n["data-address"]) > 0:
                prison_address.append(n["data-address"])
        else:
            prison_address.append("not available")
    else:
        prison_address.append("not available")
    # prisoner status
    status.append(row.find_all("td")[6].text)


# make data frame
prisoners = pd.DataFrame(
    {
        "name": name,
        "date_of_birth": date_of_birth,
        "gender": gender,
        "date_of_detention": date_of_detention,
        "charges": charges,
        "prison": prison,
        "prinson_address": prison_address,
        "status": status,
    }
)


# Replace white spaces
prisoners = prisoners.replace(r"\n", "", regex=True)
prisoners = prisoners.replace(r"^ +| +$", r"", regex=True)


# make date time
prisoners.date_of_detention = pd.to_datetime(prisoners.date_of_detention)


# get year of detention
prisoners["year_of_detention"] = prisoners.date_of_detention.dt.year


# date of detention is available for all prosioners 2020 onwards
# date of detention is unavailable for 17 instances
# prisoners["date_of_detention"].isna().value_counts()
# prisoners.isna().value_counts()

# save file
prisoners.to_csv("processed_data/viasna_data/viasna_political_prisoners.csv")


# cross check information from web archive ?
# https://web.archive.org/web/20210730173415/https://prisoners.spring96.org/en/table
