import requests
import configparser
import random
import string
import re
import os
from bs4 import BeautifulSoup
from requests_toolbelt import MultipartEncoder

# ouchn_cmid = ""
ouchn_id = ""
ouchn_sesskey = ""
ouchn_ms = ""
ouchn_host = "http://shandong.ouchn.cn"

userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36"



# 开始测验
def E(cmid):

    payload = {"cmid":cmid,"sesskey":ouchn_sesskey}
    cookies = dict(MoodleSession=ouchn_ms)
    post_url = ouchn_host + "/mod/quiz/startattempt.php"
    r = requests.post(post_url,data=payload,cookies=cookies,headers={"User-Agent":userAgent})
    return r.text
    # print(r.request.headers,r.text)

# 获取所有专题ID
def D(id):
    result = []
    test_url = ouchn_host + "/course/view.php?id=" + id + "&test=1"
    cookies = dict(MoodleSession=ouchn_ms)
    r = requests.get(test_url,cookies=cookies,headers={"User-Agent":userAgent})
    html = r.text
    soup_all = BeautifulSoup(html, 'lxml')
    soup = soup_all.find_all('div',{'class':'test'})
    for tag in soup:
        value = tag.find('p')
        if str(value).find('专题') >= 0:
            url = tag.find('a')['href']
            suffix = str(url).split('=')[1]
            result.append(suffix)
    return result

def G(index):
    cf = configparser.ConfigParser()
    cf.read("xijinping.ini")
    # cf.read("sixiangdaode.ini")
    # cf.read("zhongguojin.ini")
    cf.sections()
    value = cf.get('ANSWER',str(index))
    value = value.split(',')
    return value

# 获取题目提交参数
def B(html):
    # html = r.text
    param_list = []
    soup_all = BeautifulSoup(html, 'lxml')
    for index in range(50):
        q_id = "q" + str(index + 1)
        soup_all = BeautifulSoup(html, 'lxml')
        soup = soup_all.find(id=q_id)
        if soup is None:
            continue

        input_list_soup = soup.find_all("input",limit=5)

        for input_tag in input_list_soup:
            if input_tag.get('class') is not None :
                if input_tag.get('class')[0] == 'questionflagpostdata':
                    input_list_soup.remove(input_tag)

        for input_tag_1 in input_list_soup:
            v = (input_tag_1['name'],input_tag_1['value'])
            param_list.append(v)

    # 提交按钮参数
    next_tag = soup_all.find('input',{'name':'next'})
    param_list.append((next_tag['name'],next_tag['value']))
    attempt_tag = soup_all.find('input',{'name':'attempt'})
    thispage_tag = soup_all.find('input',{'name':'thispage'})
    nextpage_tag = soup_all.find('input',{'name':'nextpage'})
    timeup_tag = soup_all.find('input',{'name':'timeup'})
    sesskey_tag = soup_all.find('input',{'name':'sesskey'})
    slots_tag = soup_all.find('input',{'name':'slots'})
    param_list.append((attempt_tag['name'],attempt_tag['value']))
    param_list.append((thispage_tag['name'],thispage_tag['value']))
    param_list.append((nextpage_tag['name'],nextpage_tag['value']))
    param_list.append((timeup_tag['name'],timeup_tag['value']))
    param_list.append((sesskey_tag['name'],sesskey_tag['value']))
    param_list.append(('scrollpos',''))
    param_list.append((slots_tag['name'],slots_tag['value']))

    # print(param_list)
    return param_list

# 添加答案
def C(params,answer):
    # answer = [1,1]
    # answer = [1,3,0,0,1]
    i = 0
    for index in range(len(params)):
        if params[index][0].endswith('answer'):
            params[index] = (params[index][0],answer[i])
            i = i + 1
    return params

# 保存答案
def A(params):

    print(params)
    cookies = dict(MoodleSession=ouchn_ms)

    post_url = ouchn_host + "/mod/quiz/processattempt.php"
    # post_url = "http://httpbin.org/post"

    boundary_suffix = ''.join(random.sample(string.ascii_letters + string.digits, 16))
    m = MultipartEncoder(params,boundary='------WebKitFormBoundary' + boundary_suffix)

    r = requests.post(post_url,data=m.to_string(),cookies=cookies,headers={'Content-Type':m.content_type,'User-Agent':userAgent})
    
    print(r.status_code)
    # print(r.request.headers,r.request.body,r.text)

def F(cmids):

    for index in range(len(cmids)):
        html = E(cmids[index])
        params = B(html)
        param = C(params,G(index + 1))
        A(param)

    print("End")


# A(B(r.text))
# A(C(B(r.text)))
# print(G(1))

F(D(ouchn_id))





