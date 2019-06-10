#encoding=utf-8
from RankingList import RankingList
import requests
import json
import xml.etree.ElementTree as ET
from AnonymousIP import AnonymousIP

class Barrage:
    def __init__(self):
        self.rankingList = RankingList().getRankingList()
        self.list = []
        self.anony = AnonymousIP(1)


    def getCid(self,aid):
        header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
             AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
        res = requests.get("https://api.bilibili.com/x/player/pagelist?aid=" + aid + "&jsonp=jsonp",headers=header,proxies=self.anony.getProxy())
        return res.json()["data"][0]['cid']

    def getBarrages(self,aid,aid_title):
        oid = self.getCid(aid)
        # url = "https://api.bilibili.com/x/v2/dm/history?type=1&oid="+ str(oid) +"&date=2019-06-09"
        url = "https://api.bilibili.com/x/v1/dm/list.so?oid=" + str(oid)
        header = {  "Origin": "https://www.bilibili.com",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
        res = requests.get(url,headers=header,proxies=self.anony.getProxy()).content.decode()
        root = tree = ET.fromstring(res)
        #root = ET.parse(path).getroot()

        with open('barrages.txt','a+',encoding="utf-8") as f:
            for e in root.iter('d'):
                attr = e.attrib['p'].split(',')
                # 弹幕出现的时间以秒为单位
                second = attr[0]
                #弹幕类型（1-跑马灯，4-底部）
                bar_type = attr[1]
                #字体
                size = attr[2]
                #颜色
                color = attr[3]
                #Unix时间戳基准时间为 1970.01.01，日期=（Unix时间戳+83600）/86400+70365+闰天
                timestamp = attr[4]
                #弹幕池（0-普通池 1-字幕池 2-特殊池）
                bar_pool = attr[5]
                #用户id
                user_id = attr[6]
                #唯一标识
                token = attr[7]
                
                text = e.text
                
                content = str(aid) + "\t" + str(aid_title) + "\t" +  str(second) + "\t" + str(bar_type) + "\t" + str(size) + "\t" + str(color) + "\t" + str(timestamp) + "\t" \
                    + str(bar_pool) + "\t" + str(user_id) + '\t' +str(token) + '\t' + text + '\n'

                #print("content::" + content)
                f.write(content)

    def save(self):
        # for movie in self.rankingList[0:3]:
        for movie in self.rankingList:
            aid = movie['aid']
            aid_title = movie['title']
            self.getBarrages(aid,aid_title)

if __name__ == "__main__":
    Barrage().save()
