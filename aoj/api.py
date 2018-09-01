import configparser

URLS = {
        "coj" : {
            "loginUrl" : "http://192.168.9.210/acmctgu/UserAction!login.action",
            "infoUrl" : "http://192.168.9.210/acmctgu/UserAction!userInfo.action",
            "contestUrl" : "http://192.168.9.210/acmctgu/PaperAction/PaperAction!getPapers.action"  \
            + "?&selectOne=&teacherOrexam=&status=&isjava=&index=1",
            "rankUrl" : "http://192.168.9.210/acmctgu/Exam/ExamAction!showRank.action"
        },
    
}

basePath = os.environ['HOME'] + '/.aoj/'
conf = configparser.ConfigParser()
conf.read(basePath + 'base.conf')
OJ_NAME = self.conf.get('base', 'oj_name')

class API(object):
    @staticmethod
    def getCurrentUrls():
        return URLS[OJ_NAME]
        
