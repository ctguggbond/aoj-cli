import requests
import pytesseract 
from PIL import Image
from io import BytesIO
from http import cookiejar
import configparser

class RequestUtil(object):
    
    def __init__(self):
        self.header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
#            'Host': ,
#            'Referer': ,
        }        
        self.basePath = os.environ['HOME'] + '/.aoj/'
        self.conf = configparser.ConfigParser()
        self.conf.read(basePath + 'base.conf')
        self.OJ_NAME = self.conf.get('base', 'oj_name')

        self.session = requests.session()
        self.session.cookies = cookiejar.LWPCookieJar(basePath + ".cookies/" + OJ_NAME)
        self.session.cookies.load(ignore_discard=True, ignore_expires=True)

    # 解析验证码，当然只支持简单的
    def parseVerifyCode(url):
        image = Image.open(BytesIO(session.get(url).content))
        vcode = pytesseract.image_to_string(image)
        return vcode

    def doPost(url, data):
        return self.session.post(url, headers = self.header, data = data)
    
    def doGet(url, param):
        return self.session.get(url, headers = self.header, params=param)
        
