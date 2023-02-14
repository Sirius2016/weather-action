from bs4 import BeautifulSoup
import sys
import requests
 
def generate_weather_text(weather: dict) -> str:
    ret = [
        f'位置：{weather.get("province")}-{weather.get("city")}  今天：{weather.get("date")}',
        f'当前天气：{weather.get("weather")}  最低：{weather.get("low")}°C  最高：{weather.get("high")}°C',
        f'空气质量：{weather.get("airQuality")}  湿度：{weather.get("humidity")}',
        f'风向：{weather.get("wind")}  PM2.5：{weather.get("pm25")}',
    ]
    return '\n'.join(ret)
 
def get_weather(city: str) -> dict:
    url = 'http://autodev.openspeech.cn/csp/api/v2.1/weather'
    params = {
        'openId': 'aiuicus',
        'clientType': 'android',
        'sign': 'android',
        'city': city,
    }
    res = requests.get(url, params=params).json()
    return res['data']['list'][0]
 
def get_weather_text(city: str) -> str:
    weather = get_weather(city)
    return generate_weather_text(weather)
 

soup = BeautifulSoup(open('result.html'),"html.parser")
titleArr = soup.select('.u')
#标题
headerTitle = titleArr[0].get_text()
formatText = headerTitle + '\n'

#获取深圳当日天气预报
ret= [get_weather_text("深圳")]
ret_result ='\n\n'.join(ret)
#print (ret_result)
formatText += ret_result + '\n\n'

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






