import configparser
import os

basePath = os.environ['HOME'] + '/.aoj/'
# 读取基础配置
baseConf = configparser.ConfigParser()
baseConf.read(basePath + 'base.conf')
OJ_NAME = baseConf.get('base', 'oj_name')

class AojApi(object):
    # 读取 对应oj特定配置 如url信息
    ojConf = configparser.ConfigParser()
    ojConf.read(os.getcwd() + '/' + OJ_NAME + '/' + OJ_NAME + '.conf')

    def loginUrl(self):
        return self.ojConf.get('urls', 'login')
    def userInfoUrl(self):
        return self.ojConf.get('urls', 'userInfo')
    def contestUrl(self):
        return self.ojConf.get('urls', 'contest')
    def rankUrl(self):
        return self.ojConf.get('urls', 'rank')
