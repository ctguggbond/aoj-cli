import configparser
import os
from aojBase import globalVar

class AojApi(object):
    def loginUrl(self):
        return globalVar.OJ_CONF.get('urls', 'login')
    def userInfoUrl(self):
        return globalVar.OJ_CONF.get('urls', 'userInfo')
    def contestUrl(self):
        return globalVar.OJ_CONF.get('urls', 'contest')
    def rankUrl(self):
        return globalVar.OJ_CONF.get('urls', 'rank')
