"""
run following command in terminal or bash first: pip install lxml beautifulsoup4 requests pandas

Werner Eichner for Synertics 2023
"""
import requests
from bs4 import BeautifulSoup
from lxml import etree
import pandas as pd
import sys
from datetime import date, timedelta

# initializing the input parameters
product = sys.argv[1]
zone = sys.argv[2]
instrument = sys.argv[3]
time_period = sys.argv[4]

dataframes = []

start_date = date(2022, 12, 1)
end_date = date(2022, 12, 5)
delta = timedelta(days=1)
while start_date <= end_date:
    # making the requests
    url = f"https://www.omip.pt/en/dados-mercado?date={start_date}&product={product}&zone={zone}&instrument={instrument}"

    response = requests.get(url)

    # using beautiful soup and lxml tools to parse the html
    html_soup = BeautifulSoup(response.text, "html.parser")
    dom = etree.HTML(str(html_soup))

    # using XPATH to locate the rows with the information of interest
    rows = dom.xpath(f'//div[@rel="FTB - {time_period}"]//tr[@class="odd"]')

    # the logic to get the values is based on the fact that row 14 and 15 (indexed to 0) will always be columns D and D-1 respectively
    # print(rows[0].getchildren()[14:16][1].text)

    # initializing dict with the scrapped data
    year = int(start_date.strftime("%Y-%m-%d").split("-")[0])
    d_d1_dict = {"d": [], "d_1": [], "year": list(range(year + 1, year + 11))}

    # using the logic through all rows and appending values to dictionary
    for row in rows[1:]:
        d = row.getchildren()[14:16][0].text
        d_1 = row.getchildren()[14:16][1].text

        # if both are not available then raise a warning and put 0
        if d_1 == "n.a." and d == "n.a.":
            print("D and D-1 are both not available")
            d = d_1 = 0

        #where the value is "n.a." we replace that with the other column
        d = d_1 if d == "n.a." else d
        d_1 = d if d_1 == "n.a." else d_1

        # adding values to dictionary
        d_d1_dict["d"].append(float(d))
        d_d1_dict["d_1"].append(float(d_1))

    # creating and exporting the dataframe
    df = pd.DataFrame(data=d_d1_dict)
    df["prediction_day"] = start_date
    dataframes.append(df)
    start_date += delta
    
final_df = pd.concat(dataframes, axis=0)
  
csv_name = f"future-pred_{time_period}_{start_date}_{product}_{zone}_{instrument}.csv"
final_df.to_csv(csv_name, sep=",", index=False)
print(f"CSV is ready under name: {csv_name}")
    