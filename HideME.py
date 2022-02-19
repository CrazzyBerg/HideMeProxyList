import json
import urllib.parse

import requests
from bs4 import BeautifulSoup
from user_agent import generate_user_agent


class HideME:

    def __init__(self, url, count=512, max_time=0, types='hs45', anon=0):
        self.base_url = 'https://hidemy.name/'
        self.lang = 'en'
        self.url = url
        self.count = count
        self.anon = anon
        self.types = types
        self.max_time = max_time
        self.session = requests.Session()
        self.proxy_list = []

    def format(self, proxy):
        return {
            'ip': proxy[0],
            'port': proxy[1],
            'type': proxy[4],
            'max_time': proxy[3],
            'country': proxy[2],
            'anon': proxy[5],
            'last_update': proxy[6]
        }

    def gen_url(self, page=0):
        param = {}
        url = self.base_url + self.lang + self.url
        if self.max_time > 0:
            param['maxtime'] = self.max_time
        if self.types != 'hs45':
            param['type'] = self.types
        if self.anon != 0:
            param['anon'] = self.anon
        if page != 0:
            param['start'] = page
        sep = '?' if bool(param) else ''
        return url + sep + urllib.parse.urlencode(param)

    def get_connect(self, url):
        headers = {
            'User-Agent': generate_user_agent(),
            'Accept': '*/*',
            'Connection': 'keep-alive',
        }
        r = self.session.get(url=url, headers=headers, stream=True)
        if r.status_code == requests.codes.ok:
            return r.content
        else:
            print(r.status_code)
            print(r.url)

    def get_page(self):
        content = self.get_connect(self.gen_url())
        soup = BeautifulSoup(content, 'lxml')
        last_page = self.get_pagination(soup)
        if last_page is not None:
            count = 0
            proxies = []
            while True:
                if int(last_page) * 64 <= count or self.count <= count:
                    break
                else:
                    content = self.get_connect(self.gen_url(count))
                    soup = BeautifulSoup(content, 'lxml')
                    proxies.append(self.get_proxy(soup))
                    # time.sleep(0.1)
                    count += 64
            self.session.close()
            return json.dumps(proxies[0][:self.count])
        else:
            self.session.close()
            return json.dumps(self.get_proxy(soup)[:self.count])

    def get_pagination(self, soup):
        try:
            last_page = soup.find('li', attrs={'class': 'next_array'}).find_previous('li').text
        except AttributeError:
            last_page = None
        return last_page

    def get_proxy(self, soup):
        rows = soup.find('tbody').find_all('tr')
        for row in rows:
            data = row.find_all('td')
            proxies = []
            for i, v in enumerate(data):
                proxies.append(data[i].text.strip())
            self.proxy_list.append(self.format(proxies))
        return self.proxy_list

    def get(self):
        return self.get_page()