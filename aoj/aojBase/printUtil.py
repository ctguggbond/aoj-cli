import termcolor


class PrintUtil:

    @staticmethod
    def error(msg):
        print("".join([termcolor.colored("ERROR", "red"), ": ", termcolor.colored(msg, "white")]))

    @staticmethod
    def warn(msg):
        print("".join([termcolor.colored("WARN", "yellow"), ": ", termcolor.colored(msg, "white")]))

    @staticmethod
    def info(msg):
        print(termcolor.colored(msg, "green"))

    @staticmethod
    def debug(msg):
        print("".join([termcolor.colored("DEBUG", "magenta"), ": ", termcolor.colored(msg, "white")]))

    @staticmethod
    def success(msg):
        print("".join([termcolor.colored("SUCCESS", "green"), ": ", termcolor.colored(msg, "white")]))