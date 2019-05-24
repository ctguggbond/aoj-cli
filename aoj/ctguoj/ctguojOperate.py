from aojBase.aojOperate import AojOperate
from aojBase import globalVar
from aojBase.aojRequestUtil import RequestUtil
from aojBase.printUtil import PrintUtil
from aojBase.model.contest import Contest
from aojBase.model.problem import Problem
from aojBase.model.userInfo import UserInfo

from bs4 import BeautifulSoup
from aojBase.aojApi import AojApi
import getpass
import termcolor
from PIL import Image
from io import BytesIO
import pytesseract
import base64
import json
import re
import sys


class CtguojOperate(AojOperate):

    def isLogin(self):
        is_login_url = AojApi.isLoginUrl()
        resp = RequestUtil.doGet(url=is_login_url)
        soup = BeautifulSoup(resp.text, "lxml")
        islogin = soup.find_all(text='用户名')
        if islogin:
            return True
        else:
            return False

    def login(self, isauto, username, password):
        if not isauto:
            username = input(termcolor.colored('请输入用户名: ', 'cyan'))
            password = getpass.getpass(termcolor.colored('请输入密码： ', 'cyan'))

        # 验证码识别率较低..索性尝试5次
        tryloginTime = 5
        while (tryloginTime > 0):
            resp = RequestUtil.doPost(url=AojApi.loginUrl(), data=self.getLoginData(username, password))

            soup = BeautifulSoup(resp.text, "lxml")
            divlist = soup.find_all('div', class_='user')

            if len(divlist) > 3:
                info = divlist[3].font.string
                if info != "验证码有误":
                    globalVar.BASE_CONF.set('user', 'password', '')
                    with open(globalVar.BASE_CONF_PATH, 'w') as fw:
                        globalVar.BASE_CONF.write(fw)
                    PrintUtil.error(info)
                    if isauto:
                        PrintUtil.info('请使用\'coj login\'手动登录')
                    break
            else:
                PrintUtil.success("登录成功！")
                RequestUtil.session.cookies.save(ignore_discard=True, ignore_expires=True)
                # 如果是手动登录成功保存密码
                if not isauto:
                    option = input(termcolor.colored(u'\n是否保存用户名及密码？ (yes/no) ', 'cyan'))
                    if option == 'yes':
                        # 保存密码
                        try:
                            globalVar.BASE_CONF.set('user', 'username', username)
                            # 先简单base64编码加密意思意思...
                            bytesString = password.encode(encoding="utf-8")
                            encodestr = base64.b64encode(bytesString)
                            globalVar.BASE_CONF.set('user', 'password', encodestr.decode(encoding='utf-8'))
                            with open(globalVar.BASE_CONF_PATH, 'w') as fw:
                                globalVar.BASE_CONF.write(fw)
                            PrintUtil.success('保存密码成功  :)')
                        except Exception as e:
                            PrintUtil.info("保存密码失败 :(")
                            PrintUtil.error(e)
                    PrintUtil.info('\'coj list -c\'查看比赛列表.\n')
                break
            tryloginTime = tryloginTime - 1
        if tryloginTime <= 0:
            PrintUtil.error("oooops...验证码识别失败,再试试?")

    # 获取登录参数
    def getLoginData(self, username, password):
        image = Image.open(BytesIO(RequestUtil.doGet(AojApi.captchaUrl()).content))
        vcode = pytesseract.image_to_string(image)

        data = {
            'user.username': username,
            'user.userpassword': password,
            'verifycode': vcode
        }
        return data

    def getContestList(self, isAll):
        resp = RequestUtil.doGet(AojApi.contestUrl())
        jdata = json.loads(resp.text)

        datalist = jdata.get('list')
        contestList = []
        for data in datalist:
            if data['status'] == 'running' or isAll:
                c = Contest()
                c.cid = data['id']
                if data['isjava'] == '1':
                    c.ctype = 'c'
                else:
                    c.ctype = 'java'
                c.title = data['papername']
                c.endTime = data['endtime']
                c.teacherName = data['teachername']
                contestList.append(c)
        return contestList

    def getProblemList(self):
        cid = globalVar.BASE_CONF.get('contest', 'cid')  # 比赛id
        ctype = globalVar.BASE_CONF.get('contest', 'ctype')
        cpass = globalVar.BASE_CONF.get('contest', 'cpass')

        data = {'id' : cid, 'type': ctype}
        resp = RequestUtil.doGet(AojApi.pwdProblemsUrl(), data) \
            if cpass == '1' else RequestUtil.doGet(AojApi.problemsUrl(), data)
        # 解析网页数据
        soup = BeautifulSoup(resp.text, "lxml")
        # 仅获取题目和id
        pList = []
        allProblemDiv = soup.find_all('div', id=re.compile(r'title_\d*'))
        if not allProblemDiv:
            PrintUtil.warn("题目空了，你可能已经AK了.")
            sys.exit(0)
        for pdiv in allProblemDiv:
            p = Problem()
            p.pid = re.sub("\D", "", pdiv['id'])
            title = pdiv.find('div', class_='nav').string.split('.')[1].strip()
            tempStrs = title.split('(')
            p.score = int(re.sub("\D", "", tempStrs[len(tempStrs) - 1]))
            p.title = title.split('(')[0].strip()
            pList.append(p)
        # 按分数排序
        pList = sorted(pList, key=lambda pList: pList.score)
        return pList

    def getProblemInfo(self, pid):
        cid = globalVar.BASE_CONF.get('contest', 'cid')  # 比赛id
        ctype = globalVar.BASE_CONF.get('contest', 'ctype')
        cpass = globalVar.BASE_CONF.get('contest', 'cpass')

        data = {'id' : cid, 'type': ctype}
        resp = RequestUtil.doGet(AojApi.pwdProblemsUrl(), data) \
            if cpass == '1' else RequestUtil.doGet(AojApi.problemsUrl(), data)
        # 解析网页数据
        soup = BeautifulSoup(resp.text, "lxml")

        pdiv = soup.find('div', id='title_' + pid)
        if not pdiv:
            PrintUtil.error("你已经AC了或者没有该题目")
            sys.exit(0)
        p = Problem()
        p.pid = re.sub("\D", "", pdiv['id'])
        p.title = pdiv.find('div', class_='nav').string.split('.')[1].strip()
        p.timeAndMem = pdiv.find('div', class_='common').string.strip()

        contentDiv = pdiv.find_all('div')
        p.content = contentDiv[3].pre.string
        p.descr_input = contentDiv[5].pre.string
        p.descr_output = contentDiv[7].pre.string
        p.ex_input = contentDiv[9].pre.string
        p.ex_output = contentDiv[11].pre.string
        p.code = ''
        return p

    def getRankingList(self, cid):
        rankData = {"id": cid}
        resp = RequestUtil.doGet(AojApi.rankUrl(), rankData)
        soup = BeautifulSoup(resp.text, "lxml")
        rankingTr = soup.find_all('tr', id=re.compile('\d*'))
        if not rankingTr:
            PrintUtil.error("没有该比赛排名...重新选择比赛")
            sys.exit(0)

        rList = []
        for tr in rankingTr:
            stu = UserInfo()
            td = tr.find_all('td')
            stu.rank = td[0].div.string
            stu.username = td[1].div.string
            stu.name = td[2].div.string
            stu.stuid = td[3].div.string
            stu.college = td[4].div.string
            stu.major = td[5].div.string
            stu.score = td[6].div.string
            stu.subTime = td[7].div.string
            rList.append(stu)
        return rList

    # 将当前选择的比赛id 及类型保存至配置文件,方便后续操作
    ## 先放这...这块待重构
    def saveContestInfo(self, cid):
        PrintUtil.info('正在获取比赛信息...')
        resp = RequestUtil.doGet(AojApi.contestUrl())
        jdata = json.loads(resp.text)
        datalist = jdata.get('list')

        ctype = '1'  # 类型 ...1代表c 0表示java
        cpass = '0'  # 是否需要密码 0为不需要

        # 根据比赛id查找比赛类型
        for data in datalist:
            if str(data['id']) == cid:
                ctype = data['isjava']
                break
        # 判断是否需要密码
        data = {'id' : cid, 'type': ctype}
        needPasswordTest = RequestUtil.doGet(AojApi.problemsUrl(), data)

        # Struts Problem Report页面报错编码不是utf-8
        if 'ISO-8859-1' in needPasswordTest.encoding:
            PrintUtil.error('没有该比赛 -_-\"')
            return
        try:
            # 如果不需要密码就没有这个头信息会抛异常，比之前的解析内容判断速度快，虽然不雅
            hasKeyContentLength = needPasswordTest.headers['Content-Length']
            cpass = '1'
            passwd = input(termcolor.colored(u'你需要输入密码参加该比赛: ', 'green'))
            joindata = {'password' : passwd, 'id': cid}
            passwdisRight = RequestUtil.doGet('http://192.168.9.210/acmctgu/Paper/PaperAction!checkpw.action', joindata)
            if passwdisRight.text == 'no':
                PrintUtil.error('密码错误!')
                return
        except:
            pass

        # 保存比赛信息
        globalVar.BASE_CONF.set('contest', 'cid', cid)
        globalVar.BASE_CONF.set('contest', 'ctype', ctype)
        globalVar.BASE_CONF.set('contest', 'cpass', cpass)
        with open(globalVar.BASE_PATH + 'base.conf', 'w') as fw:
            globalVar.BASE_CONF.write(fw)
        self.saveProblemList()
        PrintUtil.info("设置比赛成功! 'coj list -p' 显示题目列表\n")

    def submitCode(self, code, pid):

        subData = {
            'answer': code,
            'id': pid,
            'type': globalVar.BASE_CONF.get('contest', 'ctype')
        }
        resp = RequestUtil.doPost(AojApi.submitCodeUrl(), subData)
        # {"id":"125","result":"Wrong Answer.","score":0,"time":"21:34:35"}
        try:
            jdata = json.loads(resp.text)
            result = jdata['result']
            score = jdata['score']
            time = jdata['time']
            color = "red"
            if result == "Answer Correct.":
                color = "green"

            print(termcolor.colored(result, color) + '\n' + "得分：" + termcolor.colored(str(score),
                                                                                      color) + '\n' + "提交时间：" + termcolor.colored(
                time, color))
        except:
            PrintUtil.error('oops!提交出错了，请重新提交. *_*.')

    def getPassedList(self, cid):
        resp = RequestUtil.doGet(AojApi.passedProblemUrl(), {'id': cid})
        soup = BeautifulSoup(resp.text, "lxml")
        titles = soup.find_all('div', class_='nav')
        if not titles:
            PrintUtil.error("你还没有做过此比赛的题目 :)")
            sys.exit(0)

        problemList = []
        for t in titles:
            title = t.string.strip().split('.')[1]
            tempStrs = title.split('(')
            p = Problem()
            p.score = int(re.sub("\D", "", tempStrs[len(tempStrs) - 1]))
            p.title = title.split('(')[0].strip()
            p.pid = t.string.strip().split('.')[0]
            problemList.append(p)

        return problemList

    def getPassedDetail(self, cid, pid):

        resp = RequestUtil.doGet(AojApi.passedProblemUrl(), {'id': cid})
        soup = BeautifulSoup(resp.text, "lxml")
        p = soup.find('div', class_='nav', text=re.compile(r'.*' + pid + '.*'))

        if not p:
            PrintUtil.error("没有该题目...")
            sys.exit(0)
        infolist = ['title', 'content', 'descr_input', 'descr_output', 'ex_input', 'ex_output', 'code', 'score']
        j = 0
        problem = Problem()
        problem.pid = ''
        problem.timeAndMem = ''
        for i in range(0, 31):
            s = ''
            if p.string is not None:
                s = p.string
            elif p.pre is not None:
                s = p.pre.string
            elif p.span is not None:
                s = p.span.string
            elif p.textarea is not None:
                s = p.textarea.string
            if s is not None and s.strip() != '':
                setattr(problem, infolist[j], s.strip())
                j = j + 1
            p = p.next_sibling
        return problem
