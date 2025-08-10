#using request module
import requests
import pandas as pd
import json
api_url="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DA0321EN-SkillsNetwork/labs/module%201/Accessing%20Data%20Using%20APIs/jobs.json"
r=requests.get(api_url)
data=r.json()


#using web scraping
import requests
from bs4 import BeautifulSoup
import pandas as pd
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DA0321EN-SkillsNetwork/labs/datasets/Programming_Languages.html"
page=requests.get(url).text
soup=BeautifulSoup(page,"html.parser")
df=pd.DataFrame(columns=["LanguageName","A_SAL"])
for row in soup.find("table").find_all("tr"):
    col=row.find_all("td")
    lan=col[1].text
    sal=col[3].text
    df=pd.concat([df,pd.DataFrame({"LanguageName":[lan],"A_SAL":[sal]})],ignore_index=True)
df.columns=df.iloc[0]
df=df[1:]
df = df.reset_index(drop=True)
df.to_csv("popular-languages.csv", index=False)