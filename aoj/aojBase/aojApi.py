from aojBase import globalVar


class AojApi(object):

    @staticmethod
    def getUrl(urlKey):
        return globalVar.OJ_CONF.get("urls", urlKey)
