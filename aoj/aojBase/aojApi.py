import configparser
import os
from aojBase import globalVar


class AojApi(object):

    @staticmethod
    def captchaUrl():
        return globalVar.OJ_CONF.get("urls", 'captcha')

    @staticmethod
    def isLoginUrl():
        return globalVar.OJ_CONF.get("urls", 'islogin')

    @staticmethod
    def loginUrl():
        return globalVar.OJ_CONF.get('urls', 'login')

    @staticmethod
    def userInfoUrl():
        return globalVar.OJ_CONF.get('urls', 'userInfo')

    @staticmethod
    def contestUrl():
        return globalVar.OJ_CONF.get('urls', 'contest')

    @staticmethod
    def rankUrl():
        return globalVar.OJ_CONF.get('urls', 'rank')

    @staticmethod
    def problemsUrl():
        return globalVar.OJ_CONF.get('urls', 'problems')

    @staticmethod
    def pwdProblemsUrl():
        return globalVar.OJ_CONF.get('urls', 'pwdProblems')

    @staticmethod
    def submitCodeUrl():
        return globalVar.OJ_CONF.get('urls', 'submitCode')

    @staticmethod
    def passedProblemUrl():
        return globalVar.OJ_CONF.get('urls', 'passedProblem')
