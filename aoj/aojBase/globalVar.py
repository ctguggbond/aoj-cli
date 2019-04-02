import configparser
import os

BASE_PATH = os.environ['HOME'] + '/.aoj/'
# 读取基础配置
BASE_CONF = configparser.ConfigParser()
BASE_CONF.read(BASE_PATH + 'base.conf')
OJ_NAME = BASE_CONF.get('base', 'oj_name')

# 读取 对应oj特定配置 如url信息
OJ_CONF = configparser.ConfigParser()
OJ_CONF.read(os.getcwd() + '/' + globalVar.OJ_NAME + '/' + globalVar.OJ_NAME + '.conf')
