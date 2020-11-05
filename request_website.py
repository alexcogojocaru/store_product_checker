from proxy_status import ProxyStatus
from xml_parser import XmlParser
from termcolor import colored
from bs4 import BeautifulSoup
from datetime import datetime
from log_file import LogFile
import threading
import requests
import time
import winsound
import os

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/50.0.2661.102 Safari/537.36'}
frequency = 3000
duration = 1000


class RequestWebsite:
    def __init__(self, xml_file, proxies=None):
        self.xml_parser = XmlParser(xml_file)
        self.proxies_status = ProxyStatus(proxies)
        self.product_availability = dict()
        self.proxies = proxies
        self.scanned = False
        # self.log_file = open('./logs/log.txt', 'a')
        self.log_file = LogFile()

    def run(self):
        try:
            while True:
                now = datetime.now()
                self.log_file.write_file(f'\t\t{str(now)}')
                print(f'\t\t{now}')
                self.__request_website()
                self.__print_stock()
                time.sleep(180)
                self.log_file.write_file('\n')
                print('\n\n')
        except KeyboardInterrupt:
            print(colored('Exiting...', 'red'))

    def __request_website(self):
        # if not self.scanned:
        #     proxy = self.proxies_status.scan()
        #     self.__init_proxies(proxy)
        #     self.scanned = True
        # self.__init_proxies(proxy)
        self.proxies = None

        for store in self.xml_parser.tags:
            url = store['link']

            try:
                req = requests.get(url=url, headers=HEADERS, timeout=5, proxies=self.proxies)

                if req.status_code == 200:
                    print(f'{colored("[SUCCESS]", "green")} {req.status_code} - {store["seller_name"]} [{req.elapsed.total_seconds()}s]')
                    self.log_file.write_file(f"[SUCCESS] {req.status_code} - {store['seller_name']} [{req.elapsed.total_seconds()}s]") 

                    tag_name = store['seller_name'] + ' ' + store['product_name']
                    self.product_availability[tag_name] = {'outofstock': 0, 'instock': 0}

                    soup = BeautifulSoup(req.text.encode('utf-8'), 'html.parser')
                    beep_alarm = False
                    for element in soup.findAll(store['tag'], {'class': store['status']}):
                        if str(element).find(store['out_stock']) != -1:
                            self.product_availability[tag_name]['outofstock'] += 1
                        if str(element).find(store['in_stock']) != -1:
                            self.product_availability[tag_name]['instock'] += 1
                            if not beep_alarm:
                                winsound.Beep(frequency, duration)
                                beep_alarm = True
                    if not os.path.isdir('./logs'):
                        os.mkdir('./logs')
                else:
                    raise requests.exceptions.RequestException
            except (requests.exceptions.RequestException, requests.exceptions.ProxyError):
                print(f'{colored("[FAILED]", "red")} - {store["seller_name"]}')
                self.log_file.write_file(f"[FAILED] - {store['seller_name']}")

    def __init_proxies(self, proxy):
        if proxy is not None:
            self.proxies = {
                'http': 'http://' + proxy,
                'https': 'https://' + proxy
            }
        else:
            self.proxies = None

    def __print_stock(self):
        for store in self.product_availability.keys():
            print(store)
            self.log_file.write_file(store)
            
            if self.product_availability[store]['instock'] == 0:
                print(f'\t{colored("out_of_stock", "red")}')
                self.log_file.write_file(f'\tout_of_stock')
            else:
                print(f'\tin_stock: {colored(self.product_availability[store]["instock"], "green")}')
                self.log_file.write_file(f'\tin_stock: {self.product_availability[store]["instock"]}')
            
            # self.log_file.write_file(store)
            # self.log_file.write_file(f'\tin_stock: {self.product_availability[store]["instock"]}')
            # self.log_file.write_file(f'\tout_stock: {self.product_availability[store]["outofstock"]}')
            # 
            # if self.product_availability[store]['instock'] != 0:
            #     print(f'\tin_stock: {colored(self.product_availability[store]["instock"], "green")}')
            # else:
            #     print(f'\tin_stock: {colored(self.product_availability[store]["instock"], "red")}')
            # 
            # if self.product_availability[store]['outofstock'] != 0:
            #     print(f'\tout_stock: {colored(self.product_availability[store]["outofstock"], "green")}')
            # else:
            #     print(f'\tout_stock: {colored(self.product_availability[store]["outofstock"], "red")}')
