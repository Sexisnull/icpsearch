import requests
from bs4 import BeautifulSoup
import json
import urllib
import random
import urllib3
urllib3.disable_warnings()

# china数据很不准确，建议慎用

def beianx(company_name):
    datas = []
    beianxurl = "https://www.beianx.cn/search/"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
    }
    req = requests.get(beianxurl + company_name, headers=header, timeout=5, verify=False)
    html = req.text
    soup = BeautifulSoup(html, 'lxml')
    for t in soup.find_all('tr'):
        if t.find_all('td'):
            data = {}
            if "没有" in t.find_all('td')[0].get_text().strip():
                print(company_name + "备案数量为0")
                return datas
            permit = t.find_all('td')[3].get_text().strip()
            domain = t.find_all('td')[5].get_text().strip()
            data['permit'] = permit
            data['domain'] = '.'.join(domain.split('.')[1:])
            datas.append(data)

    print(company_name + "备案数量为" + str(len(datas)))
    for d in datas:
        print("备案号：" + d['permit'])
        print("备案域名：" + d['domain'])

    return datas


def chinaz(company_name):
    datas = []
    chinazurl = "https://icp.chinaz.com/record/PageData"
    postdata = "pageNo=1&pageSize=40&kw={}".format(urllib.parse.quote(company_name))
    header = {
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36"
    }
    req = requests.post(chinazurl, headers=header, data=postdata, verify=False, timeout=5)
    data = json.loads(req.content)
    if data['data']:
        for d in data['data']:
            ld = {}
            ld['permit'] = d['permit']
            ld['domain'] = d['host']
            datas.append(ld)

    print(company_name + "的备案数量为" + str(len(datas)))
    if datas:
        for d in datas:
            print("备案号：" + d['permit'])
            print("备案域名：" + d['domain'])

    return datas


if __name__ == '__main__':
    with open('companylist.txt', 'r', encoding='utf8') as f:
        for c in f.readlines():
            try:
                i = random.randint(1, 2)
                if i == 1:
                    chinaz(c.strip())
                else:
                    beianx(c.strip())
            except Exception as e:
                print(e)
                exit()
