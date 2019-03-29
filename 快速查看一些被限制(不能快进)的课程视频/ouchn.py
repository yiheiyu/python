import os
import re
import requests
import xlwt
import datetime
import logging
import unittest
from bs4 import BeautifulSoup

# ouchn_url = ""
# # OUCHN_MS = ""
# ouchn_ms = ""
# ouchn_host = ""


logging.basicConfig(filename='ouchn.log',
                    format='[%(asctime)s-%(filename)s-%(levelname)s:%(message)s]', level=logging.DEBUG, filemode='a', datefmt='%Y-%m-%d%I:%M:%S %p')


def get_id_all(ms,url):

    try:
        html = get_html(ms,url)
        soup = BeautifulSoup(html, 'lxml')
        # print(soup.prettify())
        tag = soup.find_all('body')
        reg = r'''<li class=\"activity url modtype_url \" id=\"module-(.*?)\">'''
        p = re.findall(reg, str(tag))
        logging.info(p)
        return p
    except Exception as e:
        logging.error(e)
        return None


def get_modulename(id,ms,url):

    try:
        html = get_html(ms,url)
        soup = BeautifulSoup(html, 'lxml')
        tag = soup.find('li', {'id': 'module-' + id})
        t = tag.find('input', {'name': 'modulename'})['value']
        logging.info(t)
        return t
    except Exception as e:
        logging.error(e)
        return None


def get_sesskey(ms,url):

    try:
        html = get_html(ms,url)
        soup = BeautifulSoup(html, 'lxml')
        tag = soup.find('input', {'name': 'sesskey'})['value']
        logging.info(tag)
        return tag
    except Exception as e:
        logging.error(e)
        return None
    


def ouchn_post(session, id, sesskey,host_prefix,ms):

    try:
        post_url = "%souchn.cn/course/togglecompletion.php" % (host_prefix)
        # post_url = "http://httpbin.org/post"
        body = {'id': id, 'sesskey': sesskey, 'completionstate': '1'}
        headers = {"Cookie": "MoodleSession=" + ms}
        r = session.post(post_url, data=body, headers=headers)
        logging.info(r.headers)
        logging.info("url:" + post_url)
        return r.status_code
    except Exception as e:
        logging.error(e)
        return None


def get_html(ms,url):
    try:
        headers = {"Cookie": "MoodleSession=" + ms}
        session = requests.session()
        r = session.get(url, headers=headers)
        return r.text
    except Exception as e:
        logging.error(e)
        return None


def main():

    
    ouchn_url = input("\n请输入课程首页地址：")
    ouchn_ms = input("\n请输入账号的MoodleSession：")
    host_prefix = ouchn_url[0:ouchn_url.find('.') + 1]


    

    sesskey = get_sesskey(ouchn_ms,ouchn_url)
    session = requests.session()
    ids = get_id_all(ouchn_ms,ouchn_url)

    print("\n视频总数为 %d \n" % len(ids))

    for i in ids:
        code = ouchn_post(session, i, sesskey,host_prefix,ouchn_ms)
        print("视频ID：%s \t 视频名称：%s \t 响应结果：%s" % (i, get_modulename(i,ouchn_ms,ouchn_url), code))

    os.system("pause")




if __name__ == '__main__':
    main()
