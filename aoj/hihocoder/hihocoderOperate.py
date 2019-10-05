from aojBase.aojOperate import AojOperate
from aojBase.aojRequestUtil import RequestUtil
from aojBase.printUtil import PrintUtil
from aojBase.aojApi import AojApi
from aojBase.model.contest import Contest
from aojBase.model.problem import Problem
from bs4 import BeautifulSoup
import json


class HihocoderOperate(AojOperate):

    def isLogin(self):
        resp = RequestUtil.doGet(url=AojApi.getUrl('isLogin'))
        soup = BeautifulSoup(resp.text, "lxml")
        isNotLogin = soup.find_all(text='登录')
        if isNotLogin:
            return False
        else:
            return True

    def login(self, username, password):
        data = {
            'email': username,
            'passwd': password
        }
        resp = RequestUtil.doPost(url=AojApi.getUrl('login'), data=data)
        jdata = json.loads(resp.text)

        if jdata['code'] == 0 and jdata['response']['message'] == 'success':
            return True
        else:
            PrintUtil.error(jdata['errorMessage'])
            return False

    # 获取比赛信息
    def getContestList(self, containPassed):
        #todo 加上当前正在进行的比赛
        contestList = []
        if containPassed:
            resp = RequestUtil.doGet(AojApi.getUrl('pastContest'))
            soup = BeautifulSoup(resp.text, "lxml")
            liList = soup.find_all('li', class_='md-summary')
            for pli in liList:
                contest = Contest()
                infoDiv = pli.find('div', class_='md-summary-cnt')
                problemInfo = infoDiv.find('a')
                contest.title = problemInfo.string.strip()
                contest.cid = problemInfo['href'].split('/')[-1]
                contest.ctype = 'All'
                endTimeP = pli.find('p', class_='md-summary-etime')
                contest.endTime = endTimeP.find('span', class_='htzc').string.strip()
                contest.desc = '报名人数: ' + infoDiv.find('p', class_='hiho-member').text.strip()
                contestList.append(contest)
        return contestList[::-1]

    def getPassedDetail(self, cid, pid):
        pass

    def getPassedList(self, cid):
        pass

    def getProblemInfo(self, cid, pid):
        resp = RequestUtil.doGet(AojApi.getUrl('problemBaseUrl') + cid + '/problem/' + pid)
        soup = BeautifulSoup(resp.text, "lxml")
        p = Problem()
        p.pid = pid
        p.title = soup.find('h3', class_='panel-title').string.split(':')[1]
        pDiv = soup.find('div', id='tl-problem-content')
        limitDiv = pDiv.find('div', class_='limit')
        limitSpan = limitDiv.find_all('span')
        p.timeAndMem = '时间限制: ' + limitSpan[0].string.strip() \
                              + ' 单点时限: '+ limitSpan[1].string.strip() \
                              + ' 内存限制: '+ limitSpan[2].string.strip()
        desDiv = pDiv.find('dl', class_='des')
        tagNum = 0
        for tagNode in desDiv.div.contents:
            if tagNode.name == 'h3':
                tagNum = tagNum + 1
            if tagNum == 1:
                p.content = p.content + tagNode.text.strip()
            elif tagNum == 2:
                p.descr_input = p.descr_input + tagNode.text.strip()
            elif tagNum == 3:
                p.descr_output = p.descr_output + tagNode.text.strip()
        p.ex_input = desDiv.find_all('dd')[0].pre.string.strip()
        p.ex_output = desDiv.find_all('dd')[1].pre.string.strip()
        return p

    def getProblemList(self, cid):
        resp = RequestUtil.doGet(AojApi.getUrl('problemBaseUrl') + cid + '/problems')
        soup = BeautifulSoup(resp.text, "lxml")
        problemTr = soup.find_all('tbody')
        pList = []
        for pInfo in problemTr:
            pTd = pInfo.find_all('td')
            p = Problem()
            p.pid = pTd[1].find('a')['href'].split('/')[-1]
            p.title = pTd[1].find('a').string.strip()
            p.desc = '通过率:' + pTd[2].string.strip() + ' 提交人数:' + pTd[4].string.strip()
            pList.append(p)
        return pList

    def getRankingList(self, cid):
        pass

    def submitCode(self, code, pid):
        pass
