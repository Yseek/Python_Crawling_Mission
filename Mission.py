from bs4 import BeautifulSoup
import requests

url = 'https://weather.naver.com/today/' # 네이버 오늘의 날씨
response = requests.get(url, headers={'User-agent':'Mozilla/5.0'})
source = response.text

soup = BeautifulSoup(source, 'lxml')
##weekly > div.scroll_control.end_left > div > ul > li:nth-child(3) > div > div.cell_date
date=soup.select('div.scroll_control.end_left > div > ul > li > div > div.cell_date')
date_set=[]
for x in range(10):
    date_set.append(date[x].text[:-3])

##weekly > div.scroll_control.end_left > div > ul > li:nth-child(3) > div > div.cell_temperature > strong > span.lowest
lowest = soup.select('div.scroll_control.end_left > div > ul > li > div > div.cell_temperature > strong > span.lowest')
lowest_set=[]
for x in range(10):
    lowest_set.append(int(lowest[x].text[4:-1]))

#weekly > div.scroll_control.end_left > div > ul > li:nth-child(3) > div > div.cell_temperature > strong > span.highest
highest= soup.select('div.scroll_control.end_left > div > ul > li > div > div.cell_temperature > strong > span.highest')
highest_set=[]
for x in range(10):
    highest_set.append(int(highest[x].text[4:-1]))

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

''' 
설치된 폰트 확인
font_list = [font.name for font in fm.fontManager.ttflist]
print(font_list)
'''

plt.rcParams['font.family'] = 'gulim'
plt.rcParams["figure.figsize"] = (6,8)

ds = {
    'date' : date_set,
    'lowest' : lowest_set,
    'highest' : highest_set
}

df=pd.DataFrame(ds)

plt.plot(df['date'],df['lowest'],'bo-',label='최저온도')
for x in range(0,10):
    plt.text(x,df['lowest'][x]+0.3,df['lowest'][x],ha='center',size=15)

plt.plot(df['date'],df['highest'],'ro-',label='최고온도')
for x in range(0,10):
    plt.text(x,df['highest'][x]+0.3,df['highest'][x],ha='center',size=15)

plt.legend()
plt.grid(color='gray',axis='y',linestyle='--',alpha=0.3)
plt.title('주간 예보',size=20)
plt.yticks(range(min(lowest_set)-1,max(highest_set)+2))
plt.xticks(rotation=45)
plt.ylabel('온도')

plt.show()
