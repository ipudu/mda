import sys


class Logger:
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("mda.log", "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass
