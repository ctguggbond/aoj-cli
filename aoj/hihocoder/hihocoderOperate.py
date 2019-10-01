from aojBase.aojOperate import AojOperate
from aojBase.aojRequestUtil import RequestUtil
from aojBase.printUtil import PrintUtil
from aojBase.model.contest import Contest
from bs4 import BeautifulSoup
import json


class HihocoderOperate(AojOperate):

    def isLogin(self):
        # todo 判断当前是否登录状态 cookie是否有效
        return False

    def login(self, username, password, loginUrl):
        data = {
            'email': username,
            'passwd': password
        }
        resp = RequestUtil.doPost(url=loginUrl, data=data)
        jdata = json.loads(resp.text)

        if jdata['code'] == 0 and jdata['response']['message'] == 'success':
            return True
        else:
            PrintUtil.error(jdata['errorMessage'])
            return False

    # 获取比赛信息
    def getContestList(self, containPassed, contestUrl):

        #todo 加上当前正在进行的比赛
        contestList = []
        if containPassed:
            resp = RequestUtil.doGet(contestUrl)
            # 解析出来.. 包装到Contest 返回
            print(resp.text)

        return contestList

    def getPassedDetail(self, cid, pid):
        pass

    def getPassedList(self, cid):
        pass

    def getProblemInfo(self, pid):
        pass

    def getProblemList(self):
        pass

    def getRankingList(self, cid):
        pass

    def submitCode(self, code, pid):
        pass
