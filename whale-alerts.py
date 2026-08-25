#Librerias
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timezone

#Codigo
url_whale_alert = "https://whale-alert.io/whales.html"
response = requests.get(url_whale_alert)

print(response)
#print(response.text) #Esto muestra el coidog fuente de la pagina (HTML)
soup = BeautifulSoup(response.content, "html.parser")
table=soup.find("table")
tbody=table.find("tbody")
rows=tbody.find_all("tr")

data=[]
for row in rows:

    th = row.find("th", {"scope": "row"})
    img = th.find("img")
    coin_name = img["alt"].strip() if img else th.get_text(strip=True)
    row_data=row.find_all("td")

    json_data={
        "coin_name":coin_name,
        "know":row_data[0].text.strip(),
        "unknow":row_data[1].text.strip(),
    }
    data.append(json_data)

df=pd.DataFrame(data)
#Agregado de fecha y hora
df['timestamp'] = datetime.now(timezone.utc)
#Exportarlo a un excel
df.to_csv("data/whale_alert.csv", index=False)
df.to_json("data/whale_alert.json", orient="records", lines=True)
df.to_parquet("data/whale_alert.parquet", index=False)

print(df)