from aojBase.printUtil import PrintUtil
from aojBase import globalVar
import sys
import os
import re
import base64

arg_len = len(sys.argv)
# globalVar.OJ_NAME
module = __import__('ctguoj.ctguojOperate', globals(), locals(), ['ctguojOperate'])
ojClass = getattr(module, 'CtguojOperate')
ojOperate = ojClass()


def list_commond():
    if arg_len == 3 or arg_len == 4:
        arg2 = sys.argv[2]
        if arg2 == "-c":
            if arg_len == 4 and sys.argv[3] == '-a':
                ojOperate.showContestList(True)
            else:
                ojOperate.showContestList(False)
            return
        elif arg2 == "-p":
            ojOperate.showProblemList()
            return
    PrintUtil.error("参数错误\n")
    help_commond()


def use_commond():
    if arg_len == 3:
        arg2 = sys.argv[2]
        if re.match('^\d+$', arg2):
            ojOperate.saveContestInfo(arg2)
            return
    PrintUtil.error("参数错误")
    help_commond()


def show_commond():
    if arg_len == 3:
        arg2 = sys.argv[2]
        if re.match('^\d+$', arg2):
            ojOperate.showProblemDetail(arg2)
            return
        elif arg2 == "ranking":
            ojOperate.showRanking()
            return
    elif arg_len == 5:
        arg2 = sys.argv[2]
        arg3 = sys.argv[3]
        arg4 = sys.argv[4]
        if re.match('\d+', arg2) and arg3 == '-g' and re.match(r'^(java|c|cpp)$', arg4):
            ojOperate.showProblemDetail(arg2)
            ojOperate.genCode(arg2, arg4)
            return
    PrintUtil.error("参数错误")
    help_commond()


def submit_commond():
    if arg_len == 3:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        if arg1 == "submit":
            ojOperate.showSubmitResult(arg2)
            return
    PrintUtil.error("参数错误")
    help_commond()


def passed_commond():
    if arg_len == 2:
        ojOperate.showPassed()
        return
    elif arg_len == 3 and re.match('^\d+$', sys.argv[2]):
        ojOperate.showPassedDetail(sys.argv[2])
        return
    PrintUtil.error("参数错误")
    help_commond()


def help_commond():
    info = "\n" \
           "-----------------------help-----------------------" \
           "\n" \
           " coj list -c          | 列出所有正在进行的比赛\n" \
           " coj use id           | 根据id选择比赛\n" \
           " coj list -p          | 列出当前比赛题目\n" \
           " coj show id          | 显示id对应题目的详细信息\n" \
           " coj show id -g c     | 显示题目信息并生成c语言代码文件 可选参数cpp java\n" \
           " coj submit filename  | 提交代码文件判题\n" \
           " coj login            | 登录\n" \
           " coj help             | 显示更多帮助信息\n" \
           "\n" \
           "--------------------------------------------------\n"
    PrintUtil.info(info)


def aoj_cli_main():
    # 判断是否登录
    if arg_len >= 2 and sys.argv[1] == "login":
        ojOperate.login(False, '', '')
        sys.exit(0)
    if not os.path.exists(globalVar.BASE_PATH + ".cookies/" + globalVar.OJ_NAME):
        PrintUtil.info("欢迎使用,登录后享受丝滑刷题")
        help_commond()
        PrintUtil.info("使用\'coj login\'登录")
    elif not ojOperate.isLogin():
        # 验证用户是否已经保存密码
        try:
            username = globalVar.BASE_CONF.get('user', 'username')
            encodePassword = globalVar.BASE_CONF.get('user', 'password')
            # 解码
            password = base64.b64decode(encodePassword.encode('utf-8')).decode('utf-8')
            if username == '' or password == '':
                ojOperate.login(False, '', '')
            else:
                PrintUtil.info('登录失效，正在尝试重新登录...')
                ojOperate.login(True, username, password)
        except KeyboardInterrupt:
            pass
        except:
            PrintUtil.error("登录失败，请重新登录.")
            ojOperate.login(False, '', '')

    else:
        if arg_len < 2:
            PrintUtil.error("参数错误")
            help_commond()
            return
        arg1 = sys.argv[1]

        if arg1 == "help":
            info = "\n" \
                   " coj list -c          | 列出所有正在进行的比赛\n" \
                   " coj use id           | 根据id选择比赛\n" \
                   " coj list -p          | 列出当前比赛题目\n" \
                   " coj show id          | 显示id对应题目的详细信息\n" \
                   " coj show id -g c     | 显示题目信息并生成c语言代码文件 可选参数cpp java\n" \
                   " coj submit filename  | 提交代码文件判题\n" \
                   " coj show ranking     | 显示当前参加比赛对应的排名\n" \
                   " coj list -c -a       | 列出所有进行和已结束的比赛\n" \
                   " coj passed           | 显示所有已提交过的题目列表\n" \
                   " coj passed id        | 显示已提交题目详细信息\n" \
                   " coj login            | 登录\n" \
                   "\n" \
                   "--------------------------------------------------\n" \
                   " 更多信息: https://github.com/ctguggbond/ctguOj-cli\n"
            PrintUtil.info(info)
        elif arg1 == "list":
            list_commond()
        elif arg1 == "use":
            use_commond()
        elif arg1 == "show":
            show_commond()
        elif arg1 == "submit":
            submit_commond()
        elif arg1 == "passed":
            passed_commond()
        else:
            PrintUtil.error("参数错误")
            help_commond()
