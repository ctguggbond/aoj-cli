from aojBase.printUtil import PrintUtil
from aojBase import globalVar
from aojBase.aojApi import AojApi
from aojBase.aojRequestUtil import RequestUtil
import sys
import os
import re
import base64
import getpass
import termcolor

arg_len = len(sys.argv)


def list_commond(ojOperate):
    if arg_len == 3 or arg_len == 4:
        arg2 = sys.argv[2]
        if arg2 == "-c":
            if arg_len == 4 and sys.argv[3] == '-a':
                ojOperate.showContestList(True, AojApi.contestUrl())
            else:
                ojOperate.showContestList(False, AojApi.contestUrl())
            return
        elif arg2 == "-p":
            ojOperate.showProblemList()
            return
    PrintUtil.error("参数错误\n")
    help_commond()


def use_commond(ojOperate):
    if arg_len == 3:
        arg2 = sys.argv[2]
        if re.match('^\d+$', arg2):
            ojOperate.saveContestInfo(arg2)
            return
    PrintUtil.error("参数错误")
    help_commond()


def show_commond(ojOperate):
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


def submit_commond(ojOperate):
    if arg_len == 3:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        if arg1 == "submit":
            ojOperate.showSubmitResult(arg2)
            return
    PrintUtil.error("参数错误")
    help_commond()


def passed_commond(ojOperate):
    if arg_len == 2:
        ojOperate.showPassed()
        return
    elif arg_len == 3 and re.match('^\d+$', sys.argv[2]):
        ojOperate.showPassedDetail(sys.argv[2])
        return
    PrintUtil.error("参数错误")
    help_commond()


def test_commond(ojOperate):
    if arg_len == 3:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        if arg1 == "test":
            ojOperate.testCode(arg2)
            return
    PrintUtil.error("参数错误")
    help_commond()

def checkout_commond():
    # 切换oj
    if arg_len == 3:
        globalVar.BASE_CONF.set('base', 'oj_name', sys.argv[2])
        with open(globalVar.BASE_CONF_PATH, 'w') as fw:
            globalVar.BASE_CONF.write(fw)
        return
    PrintUtil.error("参数错误")
    help_commond()

def help_commond():
    info = "\n" \
           " aoj list -c          | 列出所有正在进行的比赛\n" \
           " aoj use id           | 根据id选择比赛\n" \
           " aoj list -p          | 列出当前比赛题目\n" \
           " aoj show id          | 显示id对应题目的详细信息\n" \
           " aoj show id -g c     | 显示题目信息并生成c语言代码文件 可选参数cpp java\n" \
           " aoj submit filename  | 提交代码文件判题\n" \
           " aoj show ranking     | 显示当前参加比赛对应的排名\n" \
           " aoj list -c -a       | 列出所有进行和已结束的比赛\n" \
           " aoj passed           | 显示所有已提交过的题目列表\n" \
           " aoj passed id        | 显示已提交题目详细信息\n" \
           " aoj login            | 登录\n" \
           " aoj checkout 'ojName'| 切换oj\n" \
           " aoj help             | 显示此帮助信息\n" \
           "\n" \
           "--------------------------------------------------\n"
    PrintUtil.info(info)
    sys.exit(0)


# 检查是否登录
def check_login(ojOperate):
    # 判断是否登录
    if not os.path.exists(globalVar.BASE_PATH + ".cookies/" + globalVar.OJ_NAME):
        logo = "" \
               "                                        \n" \
               "   █████╗      ██████╗          ██╗     \n" \
               "   ██╔══██╗    ██╔═══██╗         ██║    \n" \
               "   ███████║    ██║   ██║         ██║    \n" \
               "   ██╔══██║    ██║   ██║    ██   ██║    \n" \
               "   ██║  ██║    ╚██████╔╝    ╚█████╔╝    \n" \
               "   ╚═╝  ╚═╝     ╚═════╝      ╚════╝     \n" \

        PrintUtil.info(logo)
        PrintUtil.info("欢迎使用 aoj ,登录后享受丝滑刷题")
        PrintUtil.info("使用\'aoj help\' 查看帮助信息")
        sys.exit(0)
    elif not ojOperate.isLogin():
        # 验证用户是否已经保存密码
        try:
            username = globalVar.BASE_CONF.get('user', 'username')
            encodePassword = globalVar.BASE_CONF.get('user', 'password')
            # 解码
            password = base64.b64decode(encodePassword.encode('utf-8')).decode('utf-8')
            if username == '' or password == '':
                input_name_pass_login(ojOperate)
            else:
                # 账号密码不为空， 尝试自动登录
                PrintUtil.info('登录失效，正在尝试重新登录...')
                isSuccess = ojOperate.login(username, password, AojApi.loginUrl())
                if isSuccess:
                    # 保存cookie
                    RequestUtil.session.cookies.save(ignore_discard=True, ignore_expires=True)
                    PrintUtil.success("自动登录成功!")
                else:
                    globalVar.BASE_CONF.set('user', 'password', '')
                    with open(globalVar.BASE_CONF_PATH, 'w') as fw:
                        globalVar.BASE_CONF.write(fw)
                    PrintUtil.error("尝试自动登录失败, 手动登录 :(")
                    input_name_pass_login(ojOperate)
        except KeyboardInterrupt:
            pass
        except:
            PrintUtil.error("登录失败，请稍后重试 :<")
            sys.exit(0)


# 输入账号密码的登录
def input_name_pass_login(ojOperate):
    username = input(termcolor.colored('请输入用户名: ', 'cyan'))
    password = getpass.getpass(termcolor.colored('请输入密码： ', 'cyan'))
    loginSuccess = ojOperate.login(username, password, AojApi.loginUrl())

    if loginSuccess:
        # 保存cookie
        RequestUtil.session.cookies.save(ignore_discard=True, ignore_expires=True)
        PrintUtil.info('登录成功!')
        # 保存账号密码
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
    else:
        sys.exit(0)

def aoj_cli_main():
    if arg_len < 2:
        PrintUtil.error("参数错误")
        help_commond()
        return

    arg1 = sys.argv[1]
    # 不需要判断登录的命令

    if arg1 == "help":
        help_commond()
        sys.exit(0)
    if arg1 == "checkout":
        checkout_commond()
        sys.exit(0)

    # 获取 对应oj 的操作类
    try:
        module = __import__(globalVar.OJ_NAME + '.' + globalVar.OJ_NAME + 'Operate', globals(), locals(),
                            [globalVar.OJ_NAME + 'Operate'])
        ojClass = getattr(module, globalVar.OJ_NAME.capitalize() + 'Operate')
        ojOperate = ojClass()
    except ModuleNotFoundError:
        # todo:添加支持oj列表
        PrintUtil.error("不支持oj: " + globalVar.OJ_NAME + ", 使用 aoj checkout 'oj name' 切换")
        sys.exit(0)

    if arg1 == "login":
        input_name_pass_login(ojOperate)
        sys.exit(0)

    check_login(ojOperate)

    if arg1 == "list":
        list_commond(ojOperate)
    elif arg1 == "use":
        use_commond(ojOperate)
    elif arg1 == "show":
        show_commond(ojOperate)
    elif arg1 == "submit":
        submit_commond(ojOperate)
    elif arg1 == "passed":
        passed_commond(ojOperate)
    elif arg1 == "test":
        test_commond(ojOperate)
    else:
        PrintUtil.error("参数错误")
        help_commond()
