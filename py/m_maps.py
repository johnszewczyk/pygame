import copy
import math
import random
import time

from datetime import datetime

from m_mons import Monument
from m_tiles import *


EMOJI = {
    'BORDER': '🌳',
    'CABIN': '🏠',
    'CANOE': '🛶',
    'COBWEB': '🕸️ ',
    'DOOR': '🚪',
    'DOORKEY': '🗝️',
    'GRAVE': '🪦',
    'GOLDKEY': '🔑',
    'EMPTY': '⬛️',
    'FIELD': '🌾',
    'HEADSTONE': '🪦',
    'HUMAN': '🏃',
    'KNIFE': '🔪',
    'LIGHT': '🔦',
    'LINK': '🔗',
    'LOCK': '🔒',
    'ROCK': '🪨',
    'SAVED': '🚔',
    'SPIDER': '🕷️ ',
    'TREE': '🌳',
    'WATER': '🌊',
    'WINDOW': '🪟',
    'WOLF': '🐺',
    'WEEDS': '🌾',
    'WOODS': '🌲',
    'WRECKED': '🏚️'
}


# TILE STRUCTURES
# ------------------------------------------------------------------------------


class Cabins:
    """Organizational class to hold vars and lists of vars."""

    all_cabin_roots = []
    all_cabin_tiles = []

    cabins = [
        ["cabin_3x3_n", [
            '🏠', '🚪', '🏠',
            '🏠', '🏠', '🏠',
            '🏠', '🏠', '🏠'
        ]],
        ["cabin_3x3_s", [
            '🏠', '🏠', '🏠',
            '🏠', '🏠', '🏠',
            '🏠', '🚪', '🏠'
        ]],
        ["cabin_3x3_e", [
            '🏠', '🏠', '🏠',
            '🏠', '🏠', '🚪',
            '🏠', '🏠', '🏠'
        ]],
        ["cabin_3x3_w", [
            '🏠', '🏠', '🏠',
            '🚪', '🏠', '🏠',
            '🏠', '🏠', '🏠'
        ]],
        ["cabin_4x4_ne", [
            '🏠', '🏠', '🏠', '🚪',
            '🏠', '🏠', '🏠', '🏠',
            '🏠', '🏠', '🏠', '🏠',
            '🏠', '🏠', '🏠', '🏠'
        ]],
        ["cabin_4x4_nw", [
            '🚪', '🏠', '🏠', '🏠',
            '🏠', '🏠', '🏠', '🏠',
            '🏠', '🏠', '🏠', '🏠',
            '🏠', '🏠', '🏠', '🏠'
        ]],
        ["cabin_4x4_se", [
            '🏠', '🏠', '🏠', '🏠',
            '🏠', '🏠', '🏠', '🏠',
            '🏠', '🏠', '🏠', '🏠',
            '🏠', '🏠', '🏠', '🚪'
        ]],
        ["cabin_4x4_sw", [
            '🏠', '🏠', '🏠', '🏠',
            '🏠', '🏠', '🏠', '🏠',
            '🏠', '🏠', '🏠', '🏠',
            '🚪', '🏠', '🏠', '🏠'
        ]],
        ["cabin_courtyard", [
            '🏠', '🚪', '🏠', '🌲', '🌲', '🌲', '🏠', '🚪', '🏠',
            '🏠', '🏠', '🏠', '🌲', '🌲', '🌲', '🏠', '🏠', '🏠',
            '🏠', '🏠', '🚪', '🌲', '🌲', '🌲', '🚪', '🏠', '🏠',
            '🏠', '🏠', '🏠', '🌲', '🌲', '🌲', '🏠', '🏠', '🏠',
            '🏠', '🏠', '🏠', '🌲', '🌲', '🌲', '🏠', '🏠', '🏠',
            '🏠', '🏠', '🏠', '🏠', '🚪', '🏠', '🏠', '🏠', '🏠',
            '🏠', '🏠', '🏠', '🏠', '🏠', '🏠', '🏠', '🏠', '🏠',
            '🏠', '🏠', '🏠', '🏠', '🚪', '🏠', '🏠', '🏠', '🏠'
        ]],
        ["safehouse", [
            '🚪', '🏠', '🏠', '🚪',
            '🏠', '🏠', '🏠', '🏠',
            '🏠', '🏠', '🏠', '🏠',
            '🏠', '🏠', '🏠', '🏠',
            '🏠', '🏠', '🏠', '🏠',
            '🏠', '🏠', '🏠', '🏠',
            '🏠', '🏠', '🏠', '🚪'
        ]]
    ]

    cabin_3x3_n = [

        '🏠', '🚪', '🏠',
        '🏠', '🏠', '🏠',
        '🏠', '🏠', '🏠',

    ]
    cabin_3x3_s = [

        '🏠', '🏠', '🏠',
        '🏠', '🏠', '🏠',
        '🏠', '🚪', '🏠',

    ]
    cabin_3x3_e = [

        '🏠', '🏠', '🏠',
        '🏠', '🏠', '🚪',
        '🏠', '🏠', '🏠',

    ]

    cabin_3x3_w = [

        '🏠', '🏠', '🏠',
        '🚪', '🏠', '🏠',
        '🏠', '🏠', '🏠',

    ]
    cabin_4x4_ne = [

        '🏠', '🏠', '🏠', '🚪',
        '🏠', '🏠', '🏠', '🏠',
        '🏠', '🏠', '🏠', '🏠',
        '🏠', '🏠', '🏠', '🏠',


    ]
    cabin_4x4_nw = [

        '🚪', '🏠', '🏠', '🏠',
        '🏠', '🏠', '🏠', '🏠',
        '🏠', '🏠', '🏠', '🏠',
        '🏠', '🏠', '🏠', '🏠',


    ]

    cabin_4x4_se = [

        '🏠', '🏠', '🏠', '🏠',
        '🏠', '🏠', '🏠', '🏠',
        '🏠', '🏠', '🏠', '🏠',
        '🏠', '🏠', '🏠', '🚪',

    ]

    cabin_4x4_sw = [

        '🏠', '🏠', '🏠', '🏠',
        '🏠', '🏠', '🏠', '🏠',
        '🏠', '🏠', '🏠', '🏠',
        '🚪', '🏠', '🏠', '🏠',

    ]

    cabin_5x3_nw = [


        '🏠', '🏠', '🏠', '🏠', '🏠', '🏠',
        '🏠', '🏠', '🏠', '🏠', '🏠', '🚪',
        '🏠', '🏠', '🏠', '🏠', '🏠', '🏠',
        '🏠', '🏠', '🏠', '🌲', '🌲', '🌲',
        '🏠', '🏠', '🏠', '🌲', '🌲', '🌲',
        '🏠', '🚪', '🏠', '🌲', '🌲', '🌲',

    ]

    cabin_courtyard = [

        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🏠', '🚪', '🏠', '🌲', '🌲', '🌲', '🏠', '🚪', '🏠', '🌲',
        '🌲', '🏠', '🏠', '🏠', '🌲', '🌲', '🌲', '🏠', '🏠', '🏠', '🌲',
        '🌲', '🏠', '🏠', '🏠', '🌲', '🌲', '🌲', '🏠', '🏠', '🏠', '🌲',
        '🌲', '🏠', '🏠', '🏠', '🌲', '🌲', '🌲', '🏠', '🏠', '🏠', '🌲',
        '🌲', '🏠', '🏠', '🏠', '🏠', '🚪', '🏠', '🏠', '🏠', '🏠', '🌲',
        '🌲', '🏠', '🏠', '🏠', '🏠', '🏠', '🏠', '🏠', '🏠', '🏠', '🌲',
        '🌲', '🏠', '🏠', '🏠', '🏠', '🏠', '🏠', '🏠', '🏠', '🏠', '🌲',
        '🌲', '🏠', '🏠', '🏠', '🏠', '🏠', '🏠', '🏠', '🏠', '🏠', '🌲',
        '🌲', '🏠', '🏠', '🏠', '🏠', '🚪', '🏠', '🏠', '🏠', '🏠', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',

    ]

    safehouse = [

        '🚪', '🏠', '🏠', '🚪',
        '🏠', '🏠', '🏠', '🏠',
        '🏠', '🏠', '🏠', '🏠',
        '🏠', '🏠', '🏠', '🏠',
        '🏠', '🏠', '🏠', '🏠',
        '🏠', '🏠', '🏠', '🏠',
        '🏠', '🏠', '🏠', '🚪',



    ]

    # list of all shapes
    list_of_cabins = [
        # cabin_courtyard,
        cabin_3x3_n,
        cabin_3x3_s,
        cabin_3x3_e,
        cabin_3x3_w,
        cabin_4x4_ne,
        cabin_4x4_nw,
        cabin_4x4_se,
        cabin_4x4_sw,
        cabin_5x3_nw,
    ]

    @classmethod
    def someCabin(cls):
        """Randomly choose a monument"""
        choice = random.choice(Cabins.list_of_cabins)
        return choice


class Monuments:
    """Organizational class to hold vars and lists of vars."""

    all_monument_tiles = []

    abandoned2x2 = [
        '🏚️', '🏚️',
        '🏚️', '🏚️'
    ]

    abandoned3x3 = [

        '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🏚️', '🏚️', '🏚️', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🏚️', '🏚️', '🏚️', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🏚️', '🏚️', '🏚️', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲',

    ]

    headstones_2x2 = [

        '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🪦', '🌲', '🪦', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🪦', '🌲', '🪦', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲',

    ]

    trailer_h = [
        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🏠', '🏠', '🏠', '🏠', '🏠', '🏠', '🌲',
        '🌲', '🏠', '🏠', '🏠', '🏠', '🏠', '🏠', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🏠', '🏠', '🏠', '🏠', '🏠', '🏠', '🌲',
        '🌲', '🏠', '🏠', '🏠', '🏠', '🏠', '🏠', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',

    ]

    trailer_v = [

        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🏠', '🏠', '🌲', '🌲', '🏠', '🏠', '🌲',
        '🌲', '🏠', '🏠', '🌲', '🌲', '🏠', '🏠', '🌲',
        '🌲', '🏠', '🏠', '🌲', '🌲', '🏠', '🏠', '🌲',
        '🌲', '🏠', '🏠', '🌲', '🌲', '🏠', '🏠', '🌲',
        '🌲', '🏠', '🏠', '🌲', '🌲', '🏠', '🏠', '🌲',
        '🌲', '🏠', '🏠', '🌲', '🌲', '🏠', '🏠', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',

    ]

    cabin_in_the_woods = [

        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🌳', '🌳', '🌳', '🌲', '🌲', '🌳', '🌳', '🌳', '🌲',
        '🌲', '🌳', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌳', '🌲',
        '🌲', '🌳', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌳', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🏠', '🏠', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🏠', '🏠', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🌳', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌳', '🌲',
        '🌲', '🌳', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌳', '🌲',
        '🌲', '🌳', '🌳', '🌳', '🌲', '🌲', '🌳', '🌳', '🌳', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',


    ]

    cemetery = [
        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🔗', '🔗', '🔗', '🔗', '🔗', '🔗', '🔗', '🔗', '🔗', '🔗', '🌲', '🌲', '🔗', '🔗', '🔗', '🔗', '🔗', '🔗', '🔗', '🔗', '🔗', '🔗', '🌲',
        '🌲', '🔗', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🔗', '🌲',
        '🌲', '🔗', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🔗', '🌲',
        '🌲', '🔗', '🌲', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🌲', '🔗', '🌲',
        '🌲', '🔗', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🔗', '🌲',
        '🌲', '🔗', '🌲', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🌲', '🔗', '🌲',
        '🌲', '🔗', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🔗', '🌲',
        '🌲', '🔗', '🌲', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🌲', '🔗', '🌲',
        '🌲', '🔗', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🔗', '🌲',
        '🌲', '🔗', '🌲', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🌲', '🔗', '🌲',
        '🌲', '🔗', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🔗', '🌲',
        '🌲', '🔗', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🔗', '🌲',
        '🌲', '🔗', '🌲', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🌲', '🔗', '🌲',
        '🌲', '🔗', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🔗', '🌲',
        '🌲', '🔗', '🌲', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🌲', '🔗', '🌲',
        '🌲', '🔗', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🔗', '🌲',
        '🌲', '🔗', '🌲', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🌲', '🔗', '🌲',
        '🌲', '🔗', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🔗', '🌲',
        '🌲', '🔗', '🌲', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🪦', '🌲', '🌲', '🔗', '🌲',
        '🌲', '🔗', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🔗', '🌲',
        '🌲', '🔗', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🔗', '🌲',
        '🌲', '🔗', '🔗', '🔗', '🔗', '🔗', '🔗', '🔗', '🔗', '🔗', '🔗', '🌲', '🌲', '🔗', '🔗', '🔗', '🔗', '🔗', '🔗', '🔗', '🔗', '🔗', '🔗', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',

    ]

    deepwood_cabin = [

        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🌳', '🌳', '🌳', '🌳', '🌳', '🌳', '🌲', '🌲', '🌳', '🌳', '🌳', '🌳', '🌳', '🌳', '🌲',
        '🌲', '🌳', '🌳', '🌳', '🌳', '🌳', '🌳', '🌲', '🌲', '🌳', '🌳', '🌳', '🌳', '🌳', '🌳', '🌲',
        '🌲', '🌳', '🌳', '🌳', '🌳', '🌳', '🌳', '🌲', '🌲', '🌳', '🌳', '🌳', '🌳', '🌳', '🌳', '🌲',
        '🌲', '🌳', '🌳', '🌳', '🌳', '🌳', '🌳', '🌲', '🌲', '🌳', '🌳', '🌳', '🌳', '🌳', '🌳', '🌲',
        '🌲', '🌳', '🌳', '🌳', '🌳', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌳', '🌳', '🌳', '🌳', '🌲',
        '🌲', '🌳', '🌳', '🌳', '🌳', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌳', '🌳', '🌳', '🌳', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🏠', '🏠', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🏠', '🏠', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🌳', '🌳', '🌳', '🌳', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌳', '🌳', '🌳', '🌳', '🌲',
        '🌲', '🌳', '🌳', '🌳', '🌳', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌳', '🌳', '🌳', '🌳', '🌲',
        '🌲', '🌳', '🌳', '🌳', '🌳', '🌳', '🌳', '🌲', '🌲', '🌳', '🌳', '🌳', '🌳', '🌳', '🌳', '🌲',
        '🌲', '🌳', '🌳', '🌳', '🌳', '🌳', '🌳', '🌲', '🌲', '🌳', '🌳', '🌳', '🌳', '🌳', '🌳', '🌲',
        '🌲', '🌳', '🌳', '🌳', '🌳', '🌳', '🌳', '🌲', '🌲', '🌳', '🌳', '🌳', '🌳', '🌳', '🌳', '🌲',
        '🌲', '🌳', '🌳', '🌳', '🌳', '🌳', '🌳', '🌲', '🌲', '🌳', '🌳', '🌳', '🌳', '🌳', '🌳', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',


    ]

    grove_2x2 = [

        '🌲', '🌲', '🌲', '🌲',
        '🌲', '🌳', '🌳', '🌲',
        '🌲', '🌳', '🌳', '🌲',
        '🌲', '🌲', '🌲', '🌲',

    ]

    grove_2x2i = [

        '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🌳', '🌲', '🌳', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🌳', '🌲', '🌳', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲',

    ]

    grove_4x4 = [
        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🌳', '🌳', '🌳', '🌳', '🌲',
        '🌲', '🌳', '🌳', '🌳', '🌳', '🌲',
        '🌲', '🌳', '🌳', '🌳', '🌳', '🌲',
        '🌲', '🌳', '🌳', '🌳', '🌳', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',

    ]

    oldwell = [

        '🌲', '🪨', '🌲',
        '🪨', '🌊', '🪨',
        '🌲', '🪨', '🌲',

    ]

    orchard_4x4 = [

        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🌳', '🌲', '🌳', '🌲', '🌳', '🌲', '🌳', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🌳', '🌲', '🌳', '🌲', '🌳', '🌲', '🌳', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🌳', '🌲', '🌳', '🌲', '🌳', '🌲', '🌳', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🌳', '🌲', '🌳', '🌲', '🌳', '🌲', '🌳', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',

    ]
    shedblock_4x4 = [

        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🏠', '🏠', '🌲', '🌲', '🏠', '🏠', '🌲',
        '🌲', '🏠', '🏠', '🌲', '🌲', '🏠', '🏠', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🏠', '🏠', '🌲', '🌲', '🏠', '🏠', '🌲',
        '🌲', '🏠', '🏠', '🌲', '🌲', '🏠', '🏠', '🌲',
        '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲', '🌲',
    ]

    # water formations

    lake_4x4 = [

        '🌲', '🌊', '🌊', '🌲',
        '🌊', '🌊', '🌊', '🌊',
        '🌊', '🌊', '🌊', '🌊',
        '🌲', '🌊', '🌊', '🌲',

    ]

    lake_8x8 = [

        '🌲', '🌲', '🌊', '🌊', '🌊', '🌊', '🌲', '🌲',
        '🌲', '🌊', '🌊', '🌊', '🌊', '🌊', '🌊', '🌲',
        '🌊', '🌊', '🌊', '🌊', '🌊', '🌊', '🌊', '🌊',
        '🌊', '🌊', '🌊', '🌊', '🌊', '🌊', '🌊', '🌊',
        '🌊', '🌊', '🌊', '🌊', '🌊', '🌊', '🌊', '🌊',
        '🌊', '🌊', '🌊', '🌊', '🌊', '🌊', '🌊', '🌊',
        '🌲', '🌊', '🌊', '🌊', '🌊', '🌊', '🌊', '🌲',
        '🌲', '🌲', '🌊', '🌊', '🌊', '🌊', '🌲', '🌲',

    ]

    lake_rocky = [

        '🌲', '🌲', '🌲', '🌲', '🌲',
        '🌲', '🌊', '🪨', '🌲', '🌲',
        '🌲', '🌊', '🌊', '🪨', '🌲',
        '🌲', '🌊', '🌊', '🌊', '🌲',
        '🪨', '🌲', '🌲', '🌲', '🌲',

    ]

    list_of_monuments = [
        abandoned2x2,
        abandoned3x3,
        cabin_in_the_woods,
        cemetery,
        deepwood_cabin,
        headstones_2x2,
        grove_2x2,
        grove_2x2i,
        grove_4x4,
        lake_4x4,
        lake_8x8,
        lake_rocky,
        oldwell,
        orchard_4x4,
        shedblock_4x4,
        trailer_h,
        trailer_v,
    ]

    @classmethod
    def someMonument(cls):
        """Randomly choose a monument"""

        choice = random.choice(Monuments.list_of_monuments)

        return choice


# TILE MAP GENERATOR
# ------------------------------------------------------------------------------


class TileLand:

    tilemap = []

    tile_rate = [
        (CabinsTile, 0.5),
        (FieldsTile, 10),
        (RocksTile, 1),
        (TreesTile, 5),
        (WatersTile, 0.5),
        (WoodsTile, 40),
    ]

    # make tile rules for players and enemies

    ENEMIES_INVALID_TILES = {
        EMOJI['CABIN'],
        # EMOJI['DOOR'],
        EMOJI['LINK'],
        EMOJI['ROCK'],
        EMOJI['WATER'],
        EMOJI['WINDOW'],
        EMOJI['WRECKED'],
    }
    ENEMIES_VALID_TILES = {
        EMOJI['WOODS']
    }

    def __init__(self, gamesize, edgesize) -> None:
        # args
        self.GAMESIZE = gamesize
        self.EDGESIZE = edgesize

        # vars
        self.GRIDSIZE = self.GAMESIZE * self.GAMESIZE

        # # grid tile positions
        # self.GRID_NE = self.EDGESIZE * self.GAMESIZE - self.EDGESIZE + \
        #     self.GAMESIZE - 1
        # self.GRID_NW = self.GAMESIZE * self.EDGESIZE + self.EDGESIZE
        # self.GRID_SE = self.GAMESIZE * self.GAMESIZE - \
        #     self.EDGESIZE * self.GAMESIZE - self.EDGESIZE - 1
        # self.GRID_SW = self.GAMESIZE * self.GAMESIZE - self.EDGESIZE * \
        #     self.GAMESIZE + self.EDGESIZE - self.GAMESIZE

        # # directional offsets
        # self.PATH_N = -self.GAMESIZE
        # self.PATH_S = self.GAMESIZE
        # self.PATH_E = 1
        # self.PATH_W = -1
        # self.PATH_NE = -self.GAMESIZE + 1
        # self.PATH_NW = -self.GAMESIZE - 1
        # self.PATH_SE = self.GAMESIZE + 1
        # self.PATH_SW = self.GAMESIZE - 1

        # make game map
        self.makeLand()

    @staticmethod
    def makeEdge():
        for eachtile in Tiles.all_insts:
            eachtile.setEdge()

    def makeLand(self):
        '''Function to populate array randomly - new method using tile classes'''

        # tell Tiles class the map size data
        Tiles.GAMESIZE = self.GAMESIZE
        Tiles.EDGESIZE = self.EDGESIZE

        # make tiles in loop
        for index in range(self.GRIDSIZE):

            # generate tile type
            tile_class, _ = random.choices(
                TileLand.tile_rate, weights=[weight for _, weight in TileLand.tile_rate], k=1)[0]

            # make tile inst
            init_flag = True
            next_tile = tile_class(index, init_flag)

            # override child class edge-icon, for now
            next_tile.setEdge()

        # draw shapes on map
        pencil = ShapeMaker(self.GAMESIZE)
        pencil.populateShapes()

        # remake emoji map
        self.makeIconMap()

    def makeIconMap(self):
        print("REPORTING", len(TileLand.tilemap))

        TileLand.tilemap = []

        for eachtile in Tiles.all_insts:
            TileLand.tilemap.append(eachtile.tile_icon)
        print("REPORTING", len(TileLand.tilemap))


# TILE MAP SHAPE MAKER
# ------------------------------------------------------------------------------


class ShapeMaker:

    all_shape_posi = []

    def __init__(self, gamesize):
        # Reference to the tilemap (list of Tile instances)
        self.gamesize = gamesize

    def doesShapeFit(self, root_index, shape):
        """Function to test for edge or other shape @ [root_index] for [shape]"""

        # get size of square monument via square root
        dimension = math.sqrt(len(shape))
        dimension = int(dimension)

        deep = dimension
        wide = dimension

        for x_offset in range(wide):
            position = root_index + x_offset

            for y_offset in range(deep):
                new_index = position + y_offset * self.gamesize

                # don't draw monument if it extends beyond edge
                selected_tile = Tiles.all_insts[new_index]
                if selected_tile.tile_edge:
                    return False

                # don't draw if it overlaps another shape
                if position in self.all_shape_posi:
                    return False

        return True

    def drawShape(self, root_tile, shape):
        """Function to draw shape at position using Tile instances"""

        # Get the root index from the root_tile
        root_index = root_tile.tile_posi

        print("DRAW @", root_index)

        # Get size of square shape via square root
        dimension = len(shape)
        dimension = math.sqrt(dimension)
        dimension = int(dimension)

        # Vars to increment position
        x_offset = 0
        y_offset = 0

        loop_iter = 0
        for tile_icon in shape:
            loop_iter += 1

            # calc offset
            index = root_index + x_offset + y_offset

            # make tile based on icon
            init_flag = False
            if tile_icon == EMOJI['CABIN']:
                new_tile = CabinsTile(index, init_flag)
            elif tile_icon == EMOJI['DOOR']:
                new_tile = DoorsTile(index, init_flag)
            elif tile_icon == EMOJI['WOODS']:
                new_tile = WoodsTile(index, init_flag)

            # replace the tile; removing first will make gaps
            Tiles.all_insts[index] = new_tile

            # save index of shape-type tiles
            ShapeMaker.all_shape_posi.append(index)

            # Increment position - horizontal
            x_offset += 1

            # Increment position - vertical
            if x_offset == dimension:
                x_offset = 0
                y_offset += self.gamesize

            print("  DRAW TILE @", loop_iter, "of", len(shape),
                  new_tile.tile_posi, new_tile.tile_icon)

    def populateShapes(self):
        """Function to draw all predefined shapes to map using other funcs"""

        # Draw cabins
        loop_iter = 0
        root_tiles = copy.deepcopy(CabinsTile.all_insts)
        for cabin_tile in root_tiles:
            loop_iter += 1

            print(
                f"cabin root @ {cabin_tile.tile_posi} # {loop_iter} of {len(root_tiles)}")

            # pick shape
            shape = Cabins.someCabin()

            # does shape fit
            if not self.doesShapeFit(cabin_tile.tile_posi, shape):
                continue

            # Draw shape [index] [shape]
            self.drawShape(cabin_tile, shape)
