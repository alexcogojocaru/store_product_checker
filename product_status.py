import requests
import time
from termcolor import colored
from bs4 import BeautifulSoup
from xml_parser import XMLParser


class LogTag:
    SUCCESS = 'SUCCESS'
    FAIL = 'FAILURE'


class ProductStatuses:
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    FORMAT_STRING = 'Response [%s]: %d - %s'

    def __init__(self, xml_file):
        self.xml_parser = XMLParser(xml_file)
        self.statuses = dict()
        self.product_availability = dict()

    def scan_site(self):
        try:
            while True:
                self.__request_status()
                print(self.statuses)
                print(self.product_availability)
                print('\n\n')
                time.sleep(60)
        except KeyboardInterrupt:
            print('Exiting...\n')
    
    def __request_status(self):
        for store in self.xml_parser.tags:
            req = requests.get(store['link'], headers=self.headers)

            if req.status_code == 200:
                print(FORMAT_STRING % (store['seller_name'], req.status_code, colored(LogTag.SUCCESS, 'green')))

                with open('./response_pages/' + store['seller_name'] + '.html', 'wb') as f:
                    f.write(req.text.encode('utf-8'))
                self.statuses[store['seller_name']] = (req.status_code, time.strftime("%H:%M:%S", time.localtime()))

                tag_name = store['seller_name'] + '_' + store['product_name']
                self.product_availability[tag_name] = { 'outofstock' : 0, 'instock' : 0 }
                soup = BeautifulSoup(req.text.encode('utf-8'), 'html.parser')

                for x in soup.findAll(store['tag'], {'class' : store['status']}):
                    if str(x).find(store['out_stock']) != -1:
                        self.product_availability[tag_name]['outofstock'] += 1
                    if str(x).find(store['in_stock']) != -1:
                        self.product_availability[tag_name]['instock'] += 1
            else:
                print(FORMAT_STRING % (store['seller_name'], req.status_code, colored(LogTag.FAIL, 'red')))
                    