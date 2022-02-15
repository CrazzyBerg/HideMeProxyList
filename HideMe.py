import json
import os.path
import time
import urllib.parse

import requests
import urllib3
from bs4 import BeautifulSoup
from user_agent import generate_user_agent


class HideME:

    def __init__(self, url, page=None, max_time=0, types='hs45', anon=0):
        self.base_url = 'https://hidemy.name/'
        self.lang = 'en'
        self.url = url
        self.page = page
        self.anon = anon
        self.types = types
        self.max_time = max_time
        self.session = requests.Session()
        self.proxy_list = []
        self.get_page()

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
        if self.page is not None:
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
        if last_page != 0:
            page = int(input('Найдено {0} страниц, сколько обработать: '.format(last_page)))
            if page == '':
                page = last_page
            elif page == 0:
                page = 10
            count = 0
            proxies = []
            while True:
                if count >= int(page) * 64:
                    break
                else:
                    print('Page: {0}/{1}'.format(int(count / 64) + 1, int(page)))
                    content = content = self.get_connect(self.gen_url(count))
                    soup = BeautifulSoup(content, 'lxml')
                    proxies.append(self.get_proxy(soup))
                    time.sleep(0.1)
                    count += 64
            self.save(proxies[0])
        else:
            self.save(self.get_proxy(soup))

    def get_pagination(self, soup):
        try:
            last_page = soup.find('li', attrs={'class': 'next_array'}).find_previous('li').text
        except:
            last_page = 0
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

    def save(self, proxies):
        save = int(input("""
1 - JSON
2 - LIST
3 - IP:PORT
Сохранить данные как: """))
        try:
            check = int(input('0 - Да\n1 - Нет\n(По стандарту 1)\nНужно проверять прокси: '))
        except ValueError:
            check = 1
        if save == 1:
            self.seve_to_file('json', json.dumps(proxies))
        elif save == 2:
            proxi = ''
            for proxy in proxies:
                proxi += proxy['type'].lower() + '://' + proxy['ip'] + ':' + proxy['port'] + '\n'
            self.seve_to_file('list', proxi)
        else:
            proxi = ''
            for proxy in proxies:
                proxi += proxy['ip'] + ':' + proxy['port'] + '\n'
            self.seve_to_file('ip_port', proxi)
            if check != 1:
                self.check('ip_port')


    def check(self, filename):
        file = open(f'{filename}.txt')
        proxies = list(file)
        if os.path.isfile('good.txt'):
            os.remove('good.txt')
        for proxy in proxies:
            try:
                if self.check_proxy(proxy):
                    print('Bad proxy ' + proxy)
                else:
                    print('Good proxy ' + proxy)
                    file_with_goods = open('good.txt', 'a')
                    file_with_goods.write(proxy)
            except KeyboardInterrupt:
                print('\nExit.')
                exit()

    def check_proxy(self, proxy):
            URL = "http://google.com"
            TIMEOUT = (3.05, 27)
            try:
                session = requests.Session()
                session.headers['User-Agent'] = generate_user_agent()
                session.max_redirects = 300
                proxy = proxy.split('\n', 1)[0]
                r = session.get(URL, proxies={'http': 'http://' + proxy}, timeout=TIMEOUT, allow_redirects=True)
                print(r.status_code)
            except requests.exceptions.ConnectionError as e:
                print('Error!')
                return e
            except requests.exceptions.ConnectTimeout as e:
                print('Error,Timeout!')
                return e
            except requests.exceptions.HTTPError as e:
                print('HTTP ERROR!')
                return e
            except requests.exceptions.Timeout as e:
                print('Error! Connection Timeout!')
                return e
            except urllib3.exceptions.ProxySchemeUnknown as e:
                print('ERROR unkown Proxy Scheme!')
                return e
            except requests.exceptions.TooManyRedirects as e:
                print('ERROR! Too many redirects!')
                return e

    def seve_to_file(self, filename, proxy_list):
        if os.path.isfile(f'{filename}.txt'):
            os.remove(f'{filename}.txt')
        with open(f'{filename}.txt', 'w') as f:
            f.write(proxy_list)