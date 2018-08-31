# coding : UTF-8
import requests
import csv
import random
import time
import socket
import http.client
import json
# import urllib.request
from bs4 import BeautifulSoup

def get_content(url , data = None):
    header={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    }
    timeout = random.choice(range(80, 180))
    while True:
        try:
            rep = requests.get(url,headers = header,timeout = timeout)
            rep.encoding = 'utf-8'
            # req = urllib.request.Request(url, data, header)
            # response = urllib.request.urlopen(req, timeout=timeout)
            # html1 = response.read().decode('UTF-8', errors='ignore')
            # response.close()
            break
        # except urllib.request.HTTPError as e:
        #         print( '1:', e)
        #         time.sleep(random.choice(range(5, 10)))
        #
        # except urllib.request.URLError as e:
        #     print( '2:', e)
        #     time.sleep(random.choice(range(5, 10)))
        except socket.timeout as e:
            print( '3:', e)
            time.sleep(random.choice(range(8,15)))

        except socket.error as e:
            print( '4:', e)
            time.sleep(random.choice(range(20, 60)))

        except http.client.BadStatusLine as e:
            print( '5:', e)
            time.sleep(random.choice(range(30, 80)))

        except http.client.IncompleteRead as e:
            print( '6:', e)
            time.sleep(random.choice(range(5, 15)))

    return rep.text
    # return html_text

def get_data(html_text):
    final = []
    bs = BeautifulSoup(html_text, "html.parser")  # 创建BeautifulSoup对象
    body = bs.body # 获取body部分
    data = body.select('.table-center tbody')
    # print(data)
    trs = data[0].find_all('tr')
    # data = body.find('div', {'id': '7d'})  # 找到id为7d的div
    # ul = data.find('ul')  # 获取ul部分
    # li = ul.find_all('li')  # 获取所有的li
    for tr in trs:
        d = tr.find_all('td')
        right = ''
        if len(d) > 1:
            right = d[1].string
        if right:
            final.append(right)
    # for day in li: # 对每个li标签中的内容进行遍历
    #     temp = []
    #     date = day.find('h1').string  # 找到日期
    #     temp.append(date)  # 添加到temp中
    #     inf = day.find_all('p')  # 找到li中的所有p标签
    #     temp.append(inf[0].string,)  # 第一个p标签中的内容（天气状况）加到temp中
    #     if inf[1].find('span') is None:
    #         temperature_highest = None # 天气预报可能没有当天的最高气温（到了傍晚，就是这样），需要加个判断语句,来输出最低气温
    #     else:
    #         temperature_highest = inf[1].find('span').string  # 找到最高温
    #         temperature_highest = temperature_highest.replace('℃', '')  # 到了晚上网站会变，最高温度后面也有个℃
    #     temperature_lowest = inf[1].find('i').string  # 找到最低温
    #     temperature_lowest = temperature_lowest.replace('℃', '')  # 最低温度后面有个℃，去掉这个符号
    #     temp.append(temperature_highest)   # 将最高温添加到temp中
    #     temp.append(temperature_lowest)   #将最低温添加到temp中
    #     final.append(temp)   #将temp加到final中

    return final

def write_data(data, name):
    print(data)
    file_name = name
    with open(file_name, 'a', errors='ignore', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(data)

if __name__ == '__main__':
    payloadHeader = {
        'Content-Type': 'application/json',
    }
    for num in range(919, 921):
        url = 'http://gs.amac.org.cn/amac-infodisc/api/pof/fund?rand=0.6999640591421237&page=' + str(num) + '&size=100'
        r = requests.post(url, data=json.dumps({}), headers=payloadHeader)
        parsed_json = json.loads(r.text)
        print(parsed_json)
        for data in parsed_json['content']:
            url2 = 'http://gs.amac.org.cn/amac-infodisc/res/pof/fund/' + data['url']
            html = get_content(url2)
            result = get_data(html)
            write_data(result, 'data.csv')