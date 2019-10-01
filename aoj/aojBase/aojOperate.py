from abc import ABCMeta, abstractmethod
from aojBase.printUtil import PrintUtil
from aojBase.model.contest import Contest
from aojBase import globalVar
import pickle
import os
import re
import subprocess


class AojOperate(metaclass=ABCMeta):
    @abstractmethod
    def isLogin(self):
        """
        判断是否登录
        :return: True or False
        """

    @abstractmethod
    def login(self, username, password, loginUrl):
        """
        登录方法
        :param username: 用户名
        :param password: 密码
        :param loginUrl: 登录的url
        :return: true or false
        """

    # 获取比赛列表 isAll参数表示是否显示所有
    @abstractmethod
    def getContestList(self,  containPassed, contestUrl):
        """
        获取比赛列表
        :param containPassed: 是否获取所有比赛，包括已经结束的
        :param contestUrl: 获取比赛的url
        :return: Contest model list
        """

    @abstractmethod
    def getProblemList(self):
        """
        获取题目列表
        :return: problem list
        """

    @abstractmethod
    def getProblemInfo(self, pid):
        """
        获取题目详细信息
        :param pid: 题目id
        :return: Problem()
        """

    @abstractmethod
    def getRankingList(self, cid):
        """
        获取排名列表
        :param cid: 比赛id
        :return: UserInfo() list
        """

    @abstractmethod
    def submitCode(self, code, pid):
        """
        提交代码
        :param code: 代码文本
        :param pid:  题目id
        :return: 检测结果... 暂不返回
        """

    @abstractmethod
    def getPassedList(self, cid):
        """
        获取提交过的题目列表
        :param cid:
        :return: Problem() list

       """

    @abstractmethod
    def getPassedDetail(self, cid, pid):
        """
        获取提交过的题目详细信息
        :param cid: 比赛id
        :param pid: 题目id
        :return: Problem()
        """

    # 输出比赛列表的详细信息 isAll参数表示是否显示所有
    def showContestList(self, containPassed, contestUrl):
        contestList = self.getContestList(containPassed, contestUrl)
        for c in contestList:
            if isinstance(c, Contest):
                c.problemDetail()
            else:
                PrintUtil.error('contest type error')
                break
        print(''.join(' id' + '\t' + '{:35}'.format('名称') + '语言' +
                      '\t' + '结束时间' + '\t\t' + '出题人'))

    # 显示题目详细信息
    def showProblemList(self):

        PrintUtil.info("正在加载题目列表...")
        # 先尝试从缓存的文件中加载
        i = 1
        try:
            with open(globalVar.BASE_CONF_PATH + 'problemList', 'rb') as file_object:
                pList = pickle.load(file_object)
            for p in pList:
                print(p.problemSimple, end=' ')
                if i % 3 == 0:
                    print('')
                i = i + 1
            print('')
        except:
            # 出错就从oj线上加载
            pList = self.getProblemList()
            for p in pList:
                print(p.problemSimple(), end=' ')
                if i % 3 == 0:
                    print('')
                i = i + 1
            print('')

    # 显示排名列表
    def showRanking(self):
        cid = globalVar.BASE_CONF.get('contest', 'cid')
        PrintUtil.info("加载排名中...")
        rList = self.getRankingList(cid)
        #    rList = rList.reverse()

        for i in range(0, len(rList))[::-1]:
            rList[i].showUserInfo()

    # 显示题目详细信息
    def showProblemDetail(self, pid):
        PrintUtil.info("正在加载题目...")
        p = self.getProblemInfo(pid)
        os.system('clear')
        print(p.problemDetail())

    # 提交代码
    def showSubmitResult(self, fileName):
        pid = fileName.split('.')[0]
        if not re.match('^\d+$', pid):
            PrintUtil.error("文件命名错误，请以'id.'开头， 例: 70.简单求和.c")
            return
        try:
            f = open(fileName, "r")
        except:
            PrintUtil.error("没有找到文件.检查文件名是否有误")
            return
        code = f.read()
        f.close()

        self.submitCode(code, pid)

    # 缓存题目列表信息 todo 缓存题目的所有信息
    def saveProblemList(self):
        PrintUtil.info('正在缓存题目信息...')
        pList = self.getProblemList()
        try:
            with open(globalVar.BASE_PATH + 'problemList', 'wb') as file_object:
                pickle.dump(pList, file_object)
        except Exception as e:
            PrintUtil.error('缓存失败 :(')
            print(e)
            pass

    # 显示已经通过的题目列表
    def showPassed(self):
        cid = globalVar.BASE_CONF.get('contest', 'cid')

        i = 1
        for p in self.getPassedList(cid):
            print(p.problemSimple(), end='\t')
            if i % 3 == 0:
                print('')
            i = i + 1
        print('')

    # 生成代码模板
    def genCode(self, pid, codetype):
        PrintUtil.info('代码文件生成中...')
        p = self.getProblemInfo(pid)

        title = p.title.split('(')[0].strip()

        code = '/*' + p.problemContent() + '\n*/\n\n'
        code = re.sub(r'\r', '', code)

        ccode = '#include <stdio.h>\n\nint main(){\n\n    return 0;\n}'
        cppcode = '#include <iostream> \n\n#include <cstdio>\nusing namespace std;\nint main()\n{\n\n    return 0;\n}'
        javacode = 'import java.util.*;\n\npublic class Main{\n    public static void main(String args[]){\n\n    }\n}'

        suffix = '.c'
        if codetype == 'c':
            code = code + ccode
            suffix = '.c'
        elif codetype == 'cpp':
            suffix = '.cpp'
            code = code + cppcode
        elif codetype == 'java':
            suffix = '.java'
            code = code + javacode
        fileName = pid + '.' + title + suffix
        f = open("./" + fileName, "w")
        f.write(code)
        f.flush()
        f.close()
        PrintUtil.info('文件  [ ' + fileName + ' ]  保存成功 :) ')

    # 显示已通过题目详细信息
    def showPassedDetail(self, pid):
        cid = globalVar.BASE_CONF.get('contest', 'cid')

        problem = self.getPassedDetail(cid, pid)
        try:
            problem.code.index('输入描述')
            PrintUtil.info(problem.code)
        except:
            print(problem.problemDetail())
        PrintUtil.success(problem.score)

    def testCode(self, fileName):
        # 编译
        compilep = subprocess.Popen(['g++', fileName], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        res = ''
        for line in compilep.stdout.readlines():
            res = res + line.decode()
        if res.find('error') >= 0:
            PrintUtil.info('编译错误')
            PrintUtil.error(res)
            return
        # 执行
        ## 读取测试数据
        pid = fileName.split('.')[0]
        problem = self.getProblemInfo(pid)
        ex_input = problem.ex_input
        ex_output = problem.ex_output

        execp = subprocess.Popen(['./a.out'], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        out, err = execp.communicate(input=ex_input.encode())
        PrintUtil.info("测试输出:")
        print(out.decode(), end="")
        PrintUtil.info("正确输出:")
        print(ex_output, end="")