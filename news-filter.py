# С сайта google news (https://news.google.com) (язык и регион - English | United States) необходимо
# прокачать все статьи за последний месяц (на момент прокачки) с ключевым словом Russia.
# Затем для скачанных статей необходимо рассчитать топ-50 упоминаемых тем и представить их в виде word (tag) cloud.


import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from itertools import groupby
from wordcloud import WordCloud, STOPWORDS 
import matplotlib.pyplot as plt

def compress(items):
    for key, _ in groupby(items): yield key


url = 'https://news.google.com/search?q=Russia&hl=en-US&gl=US&ceid=US%3Aen'
res = requests.get(url)
if res.ok :
    src  = res.content
    soup = BeautifulSoup(src,'lxml')
    # находим все блоки с новостями/ отсекаем новости старее 30 дней / сохраняем заголовки
    t = datetime.strftime(datetime.today()-timedelta(days = 30),'%Y-%m-%d')
    lst = soup.find_all('article')
    headers_lst = []
    for elem in lst:
        try:
            el = elem.find('time')
            if el['datetime'] > t:
                for h in elem.find_all('a'):
                    if 'DY5T1d' in h['class']:
                        headers_lst.append(h.string)
        except:
            pass
    
    #обрабатываем найденные заголовки 
    themes_lst = []
    for s in headers_lst:
        themes_lst.append(s[s.find('Russia'):].replace(' —','').replace(' –','').replace(' -','').split())
    
    # сортируем по популярности
    themes_lst = ['Russia_'+'_'.join(x[1:3]) for x in themes_lst if len(x) >= 3]
    themes_lst = sorted(themes_lst, key=lambda x: (-themes_lst.count(x), themes_lst.index(x)))
    # убираем дубли
    themes_lst = list(compress(themes_lst))[:50]
    # создаем word cloud
    wordcloud = WordCloud(width = 800, height = 800, 
                background_color ='white', 
                stopwords = set(STOPWORDS), 
                min_font_size = 10).generate(' '.join(themes_lst)) 
    plt.figure(figsize=(40, 30))
    # Display image
    plt.imshow(wordcloud) 
    # No axis details
    plt.axis("off")
    plt.show()