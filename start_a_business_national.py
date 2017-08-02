from config import *
from urllib.parse import urlencode
import requests
from bs4 import BeautifulSoup
from requests.exceptions import ConnectionError
from requests.exceptions import Timeout
from multiprocessing import Pool
import time
import random
from datetime import datetime
import pprint
#随机UserAgent
from fake_useragent import UserAgent

ua = UserAgent()
headers = {'User-Agent': ua.random}

#构造参数访问页面
def get_most_page(start):
    try:
        data = {
            "name": "",
            "industryCode":"",
            "typeCode":"",
            "wasBindUniTechnology":"-9",
            "investStageCode":"",
            "provinceCode":"",
            "pageIndex": start,
            "pageSize": "15",
        }

        params = urlencode(data)
        base = 'http://cy.ncss.org.cn/search/projectlist?'
        url = base + params
        try:
            response = requests.get(url,headers=headers,timeout=100)
            if response.status_code == 200:
                return response.text
                time.sleep(random.choice([1,2,3,4]))
            return None

        except ConnectionError:
            print('Error occurred')
            return None

    except ConnectionError as c:
        print(c)
        pass

    except Timeout as r:
        print(r)
        pass


#解析网页中的JSON文件
def parse_page_index(html):
    try:
        date_time = datetime.now().date()
        date_time = '记录时间 ' + datetime.strftime(date_time, '%Y-%m-%d')  # 转变成str
        soup = BeautifulSoup(html,"lxml")
        project= soup.select('.search-list-item')
        for i in project:
            project_name = i.select('.project-list-item-title')[0].text
            project_school = i.select('.project-list-item-tags-text')[0].select("span")[0].text
            project_province = i.select('.project-list-item-tags-text')[0].select("span")[1].text
            project_type = i.select('.project-list-item-tags-text')[0].select("span")[2].text

            project_industry = i.select('.project-list-item-tags-img')[0].text
            project_Introduction = i.select('.project-list-item-desc')[0].text

            project_url = i.select('.project-list-info')[0].select("a")[0].get('href')
            url = 'http://cy.ncss.org.cn/' + project_url

            yield {
                'project_name': project_name,
                'project_school': project_school,
                'project_province': project_province,
                'project_type': project_type,
                'project_industry': project_industry,
                'project_Introduction': project_Introduction,
                'url': url,
                'save_date': date_time,  # 记录信息保存的日期
            }
    except IndexError as e:
        print(e)
        pass

    except TypeError as n:
        print(n)
        pass




def main(start):
    html = get_most_page(start)
    items = parse_page_index(html)
    for it in items:
        if project.update({'url': it['url']}, {'$set': it}, True):   #确认唯一的url ,用来更新数据
            pprint.pprint(it)
            print('')
            print('')


if __name__ == '__main__':
    start_time = time.clock()
    pool = Pool(processes=4)
    groups = [x for x in range(0,end+1)]
    pool.map(main,groups)# 多进程运行
    pool.close()
    pool.join()
    end_time = time.clock()
    print('\n', '程序结束', ' 共运行了 ', str(end_time - start_time), ' 秒')

