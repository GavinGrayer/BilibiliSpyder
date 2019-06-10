import requests
import random
from lxml import etree
import os


""" 
    获取髙匿ip
"""
class AnonymousIP:
    def __init__(self,pageNum):
        self.AddressIP = 'https://www.xicidaili.com/nn/' + str(pageNum)
        self.header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
        #代理ip池
        self.proxies_list = [
            {"http": "123.57.76.102:80"},
            {"http":"61.135.217.7"},
            {"http":"118.78.196.19"},
            {"http":"115.223.121.94"},
            {"http":"47.96.148.248"},
            {"http":"47.95.9.128"},
            {"http":"115.223.207.144"},
            {"http":"118.24.61.165"},
            {"http":"47.95.9.128"},
            {"http":"219.141.153.12"},
            {"http":"120.79.7.88"},
            {"http":"117.191.11.110"}
        ]


        self.ip_pools = []

    def getRandomProxy(self):
        return random.choice(self.proxies_list)



    def parseURL(self):
        res = requests.get(self.AddressIP,headers=self.header,proxies=self.getRandomProxy())
        return res.content.decode()


    def deal(self):
        html = etree.HTML(self.parseURL())
        ret = html.xpath("//table//tr[@class='odd']")
        print(ret)

        # 保存
        with open('anonymousip2.txt','a+',encoding="utf-8") as f:

            for e in ret:
                #print(e.xpath(".//text()"))
                ip = e.xpath(".//text()")[2]
                ip_type = e.xpath(".//text()")[12]
                speeds = e.xpath(".//@title")
                print(str(ip) + ":"+ip_type +":"+str(speeds))
                if(ip.strip()!="" and ip_type.strip()!="" and speeds!=""):
                    #保存小于1秒的髙匿ip
                    if(float(speeds[0].replace('秒',''))<1 and float(speeds[1].replace('秒',''))<1):
                        self.ip_pools.append({ip_type:ip})
                        #f.writelines(str(self.ip_pools))
                        f.write(ip_type + '\t' +ip + '\n')


    def get_ip_pools(self):
        print('into AnonymousIP class ....')
        self.deal()
        print('waiting ...')
        with open('./anonymousip2.txt','r',encoding="utf-8") as f:
            line = f.readline().strip().split('\t')
            while line[0]!="":
                self.ip_pools.append({line[0] : line[1]})
                line = f.readline().strip().split('\t')
        return self.ip_pools     

    '''
    def get_ip_pools(self):
        print('into AnonymousIP class ....')
        if os.path.getsize('./anonymousip.txt') == 0:
            print('loading ip ...')
            self.deal()
        else:
            print('waiting ...')
            with open('./anonymousip.txt','r',encoding="utf-8") as f:
                self.ip_pools = list(f.readlines())
        return str(self.ip_pools).replace('[{','{').replace('}]','}').split(',')
    '''
        # 返回髙匿ip字典
    def getProxy(self):
        #print(random.choice(self.get_ip_pools()))
        return eval(str(random.choice(self.get_ip_pools())))


if __name__ == "__main__":
    a = AnonymousIP(1)  #第一页
    #print(ip_pools.parseURL())
    #a.deal()
    #print(a.ip_pools)
    #print(a.get_ip_pools())
    print(a.getProxy())
