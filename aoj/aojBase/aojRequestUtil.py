import requests
import pytesseract
from PIL import Image
from io import BytesIO
from http import cookiejar
from aojBase import globalVar


class RequestUtil(object):
    header = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
        # 'Host': ,
        # 'Referer': ,
    }
    session = requests.session()
    session.cookies = cookiejar.LWPCookieJar(globalVar.BASE_PATH + ".cookies/" + globalVar.OJ_NAME)
    try:
        session.cookies.load(ignore_discard=True, ignore_expires=True)
    except:
        pass

    # 解析验证码，当然只支持简单的
    @staticmethod
    def parseVerifyCode(url):
        image = Image.open(BytesIO(RequestUtil.session.get(url).content))
        vcode = pytesseract.image_to_string(image)
        return vcode

    @staticmethod
    def doPost(url, data):
        return RequestUtil.session.post(url, headers=RequestUtil.header, data=data)

    @staticmethod
    def doGet(url, param=''):
        return RequestUtil.session.get(url, headers=RequestUtil.header, params=param)
