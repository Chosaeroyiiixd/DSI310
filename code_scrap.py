from asyncore import write
from gettext import find
from bs4 import BeautifulSoup
import requests
import csv
import pandas as pd
import openpyxl
import re
import json

title_list = []
description_list = []
datetime_list = []
time_list = []
author_list = []
all_link_list = []
link_list = []

url = requests.get('https://www.abc.net.au/news/topic/exercise-and-fitness')
url.encoding = "uft-8"
soup = BeautifulSoup(url.text, 'html.parser') 


for i in range(23):
    for c in soup.find_all('div',{'class':'_3Bajv _2FvRw ZWhbj'},limit=2000):
        title_list.append([item.text for item in c.find_all('a',{'class' : '_2VA9J u0kBv _3CtDL _1_pW8 _3Fvo9 VjkbJ'})][i])

        author_list.append([item.text for item in c.find_all('a',{'class' : 'u0kBv _3CtDL _1_pW8 _3Fvo9 _1HW1q'})][i])

        description_list.append([item.text for item in c.find_all('div',{'class' : '_1EAJU _1lk8p _2O0_n _1BqKa _3pVeq hmFfs'})][i])

        datetime_list.append([item.text for item in c.find_all('time',{'class' : '_1EAJU _30fPZ _2L258 _14LIk _3pVeq hmFfs _2F43D'})][i])

        for L in c.find_all("div",{'class':'_16eiR'}):
            all_link_list.append(str(L.find("a",{'class':'_2VA9J u0kBv _3CtDL _1_pW8 _3Fvo9 VjkbJ'}).get("href")))     
        
        link_list.append(all_link_list[i])

        time_list.append(datetime_list[i].split(' at')[1])
        datetime_list[i] = datetime_list[i].split(' at')[0]

data = {'Title' : title_list, 'Description' : description_list,'Author' : author_list ,'Date' : datetime_list, 'Time' : time_list, 'url' : link_list}
table = pd.DataFrame(data)
table['url'] = 'https://www.abc.net.au'+ table['url']

table = table.to_dict('records')

print(table)
