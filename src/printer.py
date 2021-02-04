class Printer(object):
    __msgs = []

    @classmethod
    def init(cls):
        __class__.__msgs = []

    @classmethod
    def add(cls, msg):
        __class__.__msgs.append(msg)

    @classmethod
    def out(cls):
        while __class__.__msgs:
            print(__class__.__msgs.pop(0))
