from termcolor import colored


def logger(message: str, keyword: str= "WARN"):
    if keyword == "WARN":
        print(colored('[WARN]', 'yellow'), message)
    elif keyword == "ERROR":
        print(colored('[ERROR] ' + message, 'red'))
    elif keyword == "INFO":
        print(colored('[INFO]', 'blue'), message)
