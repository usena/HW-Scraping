from bs4 import BeautifulSoup
import requests
import re
import pandas as pd 
import sys

headers = {'Accept-Language': 'en-US,en;q=0.8'}
url = 'https://novelfull.net/hot-novel'
baseURL = 'https://novelfull.net'
response = requests.get(url,headers=headers)
soup=BeautifulSoup(response.text,"html.parser")

print(response.status_code)

novels = soup.select("h3.truyen-title a")

novelTitles = []
novelLinks = []
novelDescription = []
novelRating = []
novelGenre = []

for novel in novels:
    novelTitles.append(novel.text)
    novelLinks.append(baseURL+novel['href'])

latestChapter = [chapter.text for chapter in soup.select("span.chapter-text")]

for novel in novelLinks:
    novel_response = requests.get(novel)
    novel_soup = BeautifulSoup(novel_response.text,'html.parser')
    
    storeDescDiv = novel_soup.find("div",{"class":"desc-text"})
    paragraphs = storeDescDiv.find_all("p")
    description = ' '.join([p.text.strip() for p in paragraphs])
    novelDescription.append(description)
    
    novelRating.append(novel_soup.find("div",{"class":"rate"}).find("input").get("value"))
    
    storeGenre = novel_soup.select("li.active a")
    for genre in storeGenre:
        novelGenre.append(genre.get("title"))

#print(novelGenre[0])


df = pd.DataFrame(
    {'Novel Titles':pd.Series(novelTitles),
    'Novel Rating': pd.Series(novelRating),
    'Novel Genre': pd.Series(novelGenre),
    'Novel Description': pd.Series(novelDescription),
    'Latest Chapter': pd.Series(latestChapter)}
)

print (df.to_string().encode(sys.stdout.encoding,errors='replace').decode(sys.stdout.encoding))

df.to_csv('novelFull.csv',index=False)