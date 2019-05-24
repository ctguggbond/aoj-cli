import termcolor

class Contest:

    def __init__(self):
          pass

    def problemDetail(self):
        cid = termcolor.colored(self.cid, 'magenta')
        title = termcolor.colored(self.title, 'white')
        ctype = termcolor.colored(self.ctype, 'blue')
        endTime = termcolor.colored("(" + self.endTime + ")", 'red')
        teacherName = termcolor.colored(self.teacherName, 'red')
        info = '\n'.join(['['+cid + ']' + ' ' + '{:<{l}}'.format(title,l= 50-len(title.encode('GBK'))+len(title)) + ctype + '\t' + endTime + ' '+ teacherName])
        print(info)
