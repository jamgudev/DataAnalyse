from enum import Enum

# -*- coding:utf-8 -*-


class __Color(Enum):
    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    WHITE = 37


def d(tag: str, msg: str):
    __print(tag, msg, __Color.GREEN)


def i(tag: str, msg: str):
    __print(tag, msg, __Color.WHITE)


def w(tag: str, msg: str):
    __print(tag, msg, __Color.YELLOW)


def e(tag: str, msg: str):
    __print(tag, msg, __Color.RED)


def __print(tag: str, msg: str, color: __Color):
    print(f"\033[{color.value}m[{tag}]:::>> {msg}\033[{color.value}m\033[0m\033[0m")
