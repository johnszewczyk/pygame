#!/usr/bin/python3

print("Hello")


class parent:
    instlist = []

    def __init__(self) -> None:
        parent.instlist.append(self)
        # self.__class__.instlist.append(self)

    @classmethod
    def listme(cls):
        print("parent report:")
        for each in cls.instlist:
            print(each)


class child(parent):

    instlist = []

    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def listme(cls):
        print("child report:")
        for each in cls.instlist:
            print(each)


aa = parent()
bb = parent()
cc = child()
dd = child()

parent.listme()
child.listme()
