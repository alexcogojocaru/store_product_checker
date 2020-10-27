import os
from request_website import RequestWebsite

os.system('color')

if __name__ == '__main__':
    proxy_list = list()
    with open('./proxies.txt', 'r') as f:
        proxies = f.readlines()
        for proxy in proxies:
            proxy_list.append(proxy.replace('\n', ''))

    req = RequestWebsite('./web_pages.xml', proxy_list)
    req.run()
