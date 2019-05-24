import configparser
import os

BASE_PATH = os.environ['HOME'] + '/.aoj/'
# 初始化路径
if not os.path.exists(BASE_PATH):
    os.mkdir(BASE_PATH)
if not os.path.exists(BASE_PATH + '.cookies'):
    os.mkdir(BASE_PATH + '.cookies')

# 初始化配置文件
BASE_CONF = configparser.ConfigParser()
BASE_CONF_PATH = BASE_PATH + "base.conf"
if not os.path.exists(BASE_CONF_PATH):
    # 初始化配置信息
    BASE_CONF.add_section('base')
    BASE_CONF.set('base', 'oj_name', 'ctguoj')  # 初始化oj名称

    BASE_CONF.add_section('contest')
    BASE_CONF.add_section('user')
    BASE_CONF.set('contest', 'cid', '185')  # 设置比赛id
    BASE_CONF.set('contest', 'ctype', '1')  # 设置比赛类型 0为java 1为cpp
    BASE_CONF.set('contest', 'cpass', '0')  # 设置比赛是否需要密码 0为当前比赛不需要密码
    with open(BASE_CONF_PATH, 'w') as fw:
        BASE_CONF.write(fw)

BASE_CONF.read(BASE_CONF_PATH)
OJ_NAME = BASE_CONF.get('base', 'oj_name')

# 读取 对应oj特定配置 如url信息
OJ_CONF = configparser.ConfigParser()

OJ_CONF_PATH = os.getcwd() + '/aoj/' + OJ_NAME + '/' + OJ_NAME + '.conf'
if os.path.exists(OJ_CONF_PATH):
    OJ_CONF.read(OJ_CONF_PATH)
