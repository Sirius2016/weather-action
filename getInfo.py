from bs4 import BeautifulSoup
import sys
import requests
from lxml import etree

def get_weather():
    # 城市
    global weather_text
    city = 'shenzhen'
    # 目标网址
    url = 'https://www.tianqi.com/shenzhen/7'
    # 请求头，伪装成浏览器
    headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
            }
    # 向网址发送请求并获取数据
    response = requests.get(url=url,headers=headers)
    # print(response.text)
    # 筛选信息
    data = etree.HTML(response.text)
    weather_list =  data.xpath('/html/body/div[7]/div[2]/div[2]/div/div[1]//text()')
    #print(weather_list)

    # 将主要的信息拼在一起,即拼接成一个字符串
    weather_text = ''
    for text in weather_list:
        weather_text +=text
    # 用空格替换掉字符
    print(weather_text)

if get_weather().isspace():
    get_weather()
else:
    print("获取天气数据成功...")
 
soup = BeautifulSoup(open('result.html'),"html.parser")
titleArr = soup.select('.u')
#标题
headerTitle = titleArr[0].get_text()
formatText = headerTitle + '\n'

#获取深圳当日天气预报
formatText += weather_text + '\n\n'

#新闻
newsStr = ""
newsElement = soup.select('.news-wrap > .line')
for div in newsElement:
	news = div.get_text() + '\n'
	newsStr += news
formatText += newsStr + '\n'

#历史上的今天
historyTitle = soup.select('.u')[1].get_text()
formatText += historyTitle + '\n'
historyArr = soup.select('.history-wrap > .line a')
index = 0
history = ''

for a in soup.select('.history-wrap > .line a'):
	index += 1
	history += str(index) + '. ' + a.get_text() + '\n'

formatText += history + '\n'

#时间进度条 
progress = '时间进度条: ' + soup.select('.progress-bar')[0].get_text()
progress_text = soup.select('.line')[-1].get_text()
formatText += progress + '\n'
formatText += progress_text + '\n'
filename = 'result.txt'
with open (filename,'w') as file:
    file.write(formatText)   






