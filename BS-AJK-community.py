# 使用request + BeautifulSoup提取AJK北京二手房信息
import requests
from bs4 import BeautifulSoup
import pandas as pd
# 请求URL
houses = pd.DataFrame(columns = ['city','community_name', 'address', 'date', 'price', 'compare', 'link'])
url_input = 'https://beijing.anjuke.com/community/'


# 得到页面的内容

# url = url_input
# outputdf = houses
def bs_anjuke_community(url,outputdf):
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    html=requests.get(url,headers=headers,timeout=10)
    content = html.text
    #print(content)

    # 通过content创建BeautifulSoup对象
    soup = BeautifulSoup(content, 'html.parser', from_encoding='utf-8')
    house_list=soup.find_all('div',class_="li-itemmod")   #和课上位置有点不同,这个是一页下的所有房子列表
    city=soup.find_all('div',class_="sortby")         #这个是所在城市
    for house in house_list:
        temp = {}
        temp['city'] = city[0].span.em.text.strip()
        temp['community_name'] = house.find('div',class_="li-info").a['title'].strip()
        temp['address'] = house.find('div',class_="li-info").address.text.strip()
        temp['date'] = house.find('div',class_="li-info").p.text.strip()
        temp['link'] = house.find('div',class_="li-info").a['href'].strip()
        temp['price'] = house.find('div',class_="li-side").text.split()[0]
        temp['compare'] = house.find('div',class_="li-side").text.split()[2]
        outputdf = outputdf.append(temp,ignore_index=True)
    return outputdf
# urls = [url_input]    #制作循环页面url
for i in range(2,3):                  #循环制作N页，目前是10
    urls.append(str(urls[0]+'p'+str(i)))
for u in urls:
    houses = bs_anjuke_community(u,houses)

houses.to_csv('anjuke-BS.csv', index=False)

df_check = pd.read_csv('./anjuke-BS.csv')
