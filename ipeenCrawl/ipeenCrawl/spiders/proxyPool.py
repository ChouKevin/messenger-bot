import os
import json
import requests
from threading import Timer
from bs4 import BeautifulSoup

class proxyPool(object):
    """docstring for proxyPool"""
    def __init__(self, **arg):
        super(proxyPool, self).__init__()
        self.arg = arg
        self.isRunning = True

    def auto_update_proxy(self):
        if self.isRunning :
            print("Update Proxy Pool......\n")
            proxyList = self.getProxy()
            self.writeProxy(data = proxyList)
            Timer(600, self.auto_update_proxy, ()).start()
        else:
            print('Close Updata Proxy List......\n')
    
    def run(self):
        Timer(1, self.auto_update_proxy, ()).start()

    def getProxy(self, url = 'https://free-proxy-list.net/'):
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        Stable = soup.select('table.table tbody tr td')
        proxyDict = {}
        proxyList = []
        for item in [Stable[x:x+8] for x in range(0, len(Stable), 8)]:
            proxyDict['ip'] = item[0].get_text()
            proxyDict['port'] = item[1].get_text()
            proxyDict['country'] = item[2].get_text()
            proxyDict['level'] = item[4].get_text()
            proxyDict['https'] = item[6].get_text()
            proxyList.append(proxyDict.copy())
        return proxyList

    def writeProxy(self, data, path = ""):
        with open(os.path.join(path, 'proxyList.txt'), 'w+') as outFile:
            json.dump(data, outFile)