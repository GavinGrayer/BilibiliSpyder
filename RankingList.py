import requests
import json


class RankingList:
    def __init__(self):
        self.url = "https://api.bilibili.com/x/web-interface/ranking"
        self.header = {
            "Referer": "https://www.bilibili.com/ranking?spm_id_from=333.334.b_62616e6e65725f6c696e6b.11",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
         AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"}
    
    def getParams(self):
        return {"rid": "0",
                "day": "3",
                "type": "1",
                "arc_type": "0",
                "jsonp": "jsonp"}

    def getRankingList(self):
        res = requests.get(self.url,params=self.getParams(),headers=self.header)
        return json.loads(res.content.decode())["data"]["list"]


if __name__ == "__main__":
    dict = RankingList().getRankingList()
    print(dict[1])
