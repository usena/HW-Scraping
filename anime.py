from bs4 import BeautifulSoup
import requests
import re
import pandas as pd 

#NOTE: THESE COLUMNS AREN'T RELATED!!!

headers = {'Accept-Language': 'en-US,en;q=0.8'}
url = 'https://myanimelist.net/'
response = requests.get(url,headers=headers)
soup=BeautifulSoup(response.text,"html.parser")

print(response.status_code)

headers = [head.text for head in soup.select("h2.index_h2_seo")]

animeList1 = []
list1 = soup.select("h3.h3_side a")
for anime in list1:
    animeList1.append(anime.text)

animeList2 = [anime.text for anime in soup.select("h3.recommendations_h3 a")]

news = [info.text for info in soup.select("div.text p")]

images = []
images_headers = soup.select("li.btn-anime img")
for img in images_headers:
    images.append(img.get("data-src"))


#print(images[0])

df = pd.DataFrame(
    {'Headers':pd.Series(headers),
    'News': pd.Series(news),
    'Anime List 1': pd.Series(animeList1),
    'Anime List 2': pd.Series(animeList2),
    'Images': pd.Series(images)}
)

print (df)

df.to_csv('novelFull.csv',index=False)