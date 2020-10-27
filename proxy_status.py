import concurrent.futures
import requests
from termcolor import colored

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/50.0.2661.102 Safari/537.36'}


class ProxyStatus:
    def __init__(self, proxies: list, dummy_url='https://httpbin.org/ip'):
        self.proxies = proxies
        self.proxies_valid = set()
        self.dummy_url = dummy_url

    def scan(self):
        self.__start()
        if len(self.proxies_valid) != 0:
            return self.proxies_valid.pop()
        return None

    def __start(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.__check_status, self.dummy_url, proxy) for proxy in self.proxies]

    def __check_status(self, url, proxy):
        proxy_dict = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy
        }
        try:
            req = requests.get(url=url, headers=HEADERS, timeout=1, proxies=proxy_dict)
            self.proxies_valid.add(proxy)
            print(f'{colored("[SUCCESS]", "green")} - {proxy}')
        except requests.exceptions.RequestException:
            print(f'{colored("[FAILED]", "red")} - {proxy}')
