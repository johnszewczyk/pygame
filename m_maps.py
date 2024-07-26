import math
import random

from datetime import datetime


class Tiles:
    """Unused class"""

    all_calls = 0
    all_instances = []

    def __init__(self) -> None:

        Tiles.all_calls += 1
        Tiles.all_instances.append(self)

        self.serial = Tiles.all_calls
        self.ipos = Tiles.all_calls - 1
        self.xpos = None
        self.ypos = None
        # self.icon = tileicon
        # self.type = tiletype

        pass

    @classmethod
    def factory(quantity):
        for each in range(quantity):
            pass


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
        cabin_courtyard,
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


class MapData:

    all_calls = 0
    all_instances = []

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

    # make tile rules for players and enemies

    PLAYERS_INVALID_TILES = {
        EMOJI['GRAVE'],
        EMOJI['LINK'],
        EMOJI['ROCK'],
        EMOJI['TREE'],
        EMOJI['WINDOW'],
    }
    ENEMIES_INVALID_TILES = {
        EMOJI['CABIN'],
        EMOJI['DOOR'],
        EMOJI['LINK'],
        EMOJI['ROCK'],
        EMOJI['WATER'],
        EMOJI['WINDOW'],
        EMOJI['WRECKED'],
    }
    ENEMIES_VALID_TILES = {
        EMOJI['WOODS']
    }

    @staticmethod
    def getDimensions(shape):
        """Function to calc dimensions of shape in string-type variable."""
        shape = shape.strip()

        # Initialize width counter
        width = 0

        # get width
        for char in shape.splitlines():
            if char != '\n':  # Check if character is not a newline
                width += 1
            else:
                break

        # get height
        height = len(shape.splitlines())

        return width, height

    def exportTextFile(self):
        """Write tile map to .txt file in path."""

        date_str = datetime.now().strftime("%y%m%d-%H:%M:%S.%f")
        filename = f"{date_str}_tilemap.txt"

        # Open the file for writing in text mode
        with open(filename, 'w') as file:
            # Need array dimension to write lines
            size = len(self.tilemap)
            size = math.sqrt(size)
            size = int(size)

            # Write each tile to the file
            for line in range(size):
                for item in self.tilemap[line * size:(line + 1) * size]:
                    file.write(item)
                # Add a newline character at the end of each line
                file.write('\n')

    def getTileType(self, index):
        """Function to check tile type at index ARG1"""
        return self.tilemap[index]

    def index2xy(self, index):
        x = index % self.GAMESIZE
        y = index // self.GAMESIZE
        return x, y

    def xy2Index(self, x, y):
        index = y * self.GAMESIZE + x
        return index

    def isEdgeIndex(self, index):
        '''
        Checks if a given index corresponds to a tile on the edge of the grid.

        Args:
            gamesize: The size of the game grid (number of tiles along one edge).
            edgesize: The size of the edge (number of tiles considered as edge).
            index: The index of the tile to check.

        Returns:
            True if the tile is on the edge, False otherwise.
        '''

        x = index % self.GAMESIZE
        y = index // self.GAMESIZE

        a = x < self.EDGESIZE or x >= (
            self.GAMESIZE - self.EDGESIZE)
        b = y < self.EDGESIZE or y >= (
            self.GAMESIZE - self.EDGESIZE)

        return a or b

    def isCabinTile(self, index):
        if self.tilemap[index] == MapData.EMOJI["CABIN"]:
            return True
        return False

    def isFloorTile(self, index):
        """Checks if a cabin tile is a floor tile (surrounded by cabin or door tiles)."""
        if self.tilemap[index] != MapData.EMOJI["CABIN"]:
            return False

        for offset in self.COMPASS_8:
            # Check for neighbors that are not walls or doors, which would make it a floor
            if self.tilemap[index + offset] not in (MapData.EMOJI["CABIN"], MapData.EMOJI["DOOR"]):
                return False
        return True

    def isWallTile(self, index):
        """Checks if a cabin tile is a wall tile (adjacent to a non-cabin tile)."""
        if self.tilemap[index] != MapData.EMOJI["CABIN"]:
            return False

        for offset in self.COMPASS_8:
            # Check for at least one neighbor that is not a cabin tile
            if self.tilemap[index + offset] not in [MapData.EMOJI["CABIN"], MapData.EMOJI["DOOR"]]:
                return True
        return False

    def echoTileMap(self):
        """Draw tile map to terminal"""

        # need array dimension to draw lines
        size = len(self.tilemap)
        size = math.sqrt(size)

        print()

        line = 0
        for item in self.tilemap:
            line += 1
            print(item, end='')
            if line == size:
                line = 0
                print('')

    # CANVAS-TYPE FUNCTIONS

    def doesShapeFit(self, root_index, shape):
        """Function to test for edge or other shape @ [root_index] for [shape]"""

        # get size of square monument via square root
        dimension = math.sqrt(len(shape))
        dimension = int(dimension)

        deep = dimension
        wide = dimension

        for w in range(wide):
            position = root_index + w

            for h in range(deep):
                new_index = position + h * self.GAMESIZE

                # don't draw monument if it extends beyond edge
                if self.isEdgeIndex(new_index):
                    return False

                # don't draw if it overlaps another shape
                if position in self.all_shapes:
                    return False

        return True

    def drawShape(self, root_index, shape):
        """Function to draw shape at position"""

        # get size of square shape via square root
        dimension = len(shape)
        dimension = math.sqrt(dimension)
        dimension = int(dimension)

        # vars to increment position
        horizontal_offset = 0
        vertical_offset = 0
        index = 0

        for tile in shape:

            # calc offset - horizontally
            index = root_index + horizontal_offset + vertical_offset

            # save tile data as a monument - to stop overlap later
            self.all_shapes.append(index)

            # draw tile at offset
            self.tilemap[index] = tile

            # increment position - horizontal
            horizontal_offset += 1

            # increment position - vertical
            if horizontal_offset == dimension:
                horizontal_offset = 0
                vertical_offset += self.GAMESIZE

    def populateShapes(self):
        """Function to draw all predefined shapes to map using other funcs"""

        # draw cabins
        for root_index in self.tilelist_water:

            # pick random shape
            shape = Cabins.someCabin()

            # does shape fit?
            if not self.doesShapeFit(root_index, shape):
                continue

            # draw shape
            self.drawShape(root_index, shape)

        # draw monuments
        for root_index in self.tilelist_cabin:

            # pick random shape
            shape = Monuments.someMonument()

            # does shape fit?
            if not self.doesShapeFit(root_index, shape):
                continue

            # draw shape
            self.drawShape(root_index, shape)

    def drawRect(self, index, wide, deep, value):
        '''Function to draw a rectangle of [value] from [index] on self-map'''

        # test area for edge; stop draw if object extends to edge tile

        for w in range(wide):
            position = index + w

            # for height...
            for h in range(deep):
                new_index = position + h * self.GAMESIZE

                if self.isEdgeIndex(new_index):
                    return

        # calculate positions and write

        # for width...
        for w in range(wide):
            position = index + w

            # for height...
            for h in range(deep):
                new_index = position + h * self.GAMESIZE

                # draw tile
                self.tilemap[new_index] = value

                # # draw tile
                # if not self.isEdgeIndex(new_index):
                #     self.tilemap[new_index] = value

    def drawRectOmni(self, index, wide, deep, value, direction):
        '''Function to draw a rectangle of [value] from [index] on self-map'''

        # Error handling for invalid directions
        if direction not in ["downright", "upleft", " downright", "upright", "downleft"]:
            print(
                "Invalid direction. Please use downright, upleft, downright, upright, or downleft.")
            return

        # Calculate positions based on direction
        if direction == "downright":
            for w in range(wide):
                position = index + w
                for h in range(deep):
                    newindex = position + h * self.GAMESIZE
                    self.tilemap[newindex] = value
        elif direction == "upleft":
            for w in range(wide):
                position = index - w
                for h in range(deep):
                    newindex = position - h * self.GAMESIZE
                    self.tilemap[newindex] = value
        elif direction == "upright":  # Corrected logic for upright
            for w in range(wide):
                position = index + w  # Start from top-left corner
                for h in range(deep):
                    newindex = position - h * self.GAMESIZE
                    self.tilemap[newindex] = value
        elif direction == "downleft":
            for w in range(wide):
                position = index + w  # Corrected logic for downleft
                for h in range(deep):
                    newindex = position + h * self.GAMESIZE
                    self.tilemap[newindex] = value

    def makeDoor(self, tall, wide):
        """Function to select center tile OR both end tiles of line segment"""
        for index in self.tilelist_cabin:

            # north wall - center
            if not wide % 2 == 0:
                door_n = index + (wide // 2)
                if self.tilemap[door_n + self.PATH_N] is self.EMOJI['WOODS']:
                    self.tilemap[door_n] = self.EMOJI['DOOR']

            # south wall - center
            if not wide % 2 == 0:
                door_s = index + self.GAMESIZE * (tall - 1) + (wide // 2)
                if self.tilemap[door_s + self.PATH_S] is self.EMOJI['WOODS']:
                    self.tilemap[door_s] = self.EMOJI['DOOR']

            # east wall - center
            if not tall % 2 == 0:
                door_e = index + self.GAMESIZE * (tall // 2) + (wide - 1)
                if self.tilemap[door_e + self.PATH_E] is self.EMOJI['WOODS']:
                    self.tilemap[door_e] = self.EMOJI['DOOR']

            # west wall - center
            if not tall % 2 == 0:
                door_w = index + self.GAMESIZE * (tall // 2)
                if self.tilemap[door_w + self.PATH_W] is self.EMOJI['WOODS']:
                    self.tilemap[door_w] = self.EMOJI['DOOR']

                # north-east corner

                # south-east corner

                # north-west corner

                # south-west corner

                # if tall % 2 == 0 and wide % 2 == 0:

                #     # calc door tile - corner of wall
                #     door_nw = index
                #     door_sw = index + self.GAMESIZE * (tall - 1)
                #     door_ne = index + wide - 1
                #     door_se = index + self.GAMESIZE * (tall - 1) + wide - 1

                #     # save door tile to map
                #     if self.tilemap[door_nw + self.PATH_W] is MapData.EMOJI['WOODS']:
                #         self.tilemap[door_nw] = MapData.EMOJI['DOOR']
                #     if self.tilemap[door_ne + self.PATH_N] is MapData.EMOJI['WOODS']:
                #         self.tilemap[door_ne] = MapData.EMOJI['DOOR']
                #     if self.tilemap[door_se + self.PATH_E] is MapData.EMOJI['WOODS']:
                #         self.tilemap[door_se] = MapData.EMOJI['DOOR']
                #     if self.tilemap[door_sw + self.PATH_S] is MapData.EMOJI['WOODS']:
                #         self.tilemap[door_sw] = MapData.EMOJI['DOOR']

                # else:

                #     # calc door tile - middle of wall
                #     door_n = index + (wide // 2)
                #     door_s = index + self.GAMESIZE * (tall - 1) + (wide // 2)
                #     door_e = index + self.GAMESIZE * (tall // 2) + (wide - 1)
                #     door_w = index + self.GAMESIZE * (tall // 2)

                #     if self.tilemap[door_n + self.PATH_N] is self.EMOJI['WOODS']:
                #         self.tilemap[door_n] = self.EMOJI['DOOR']
                #     if self.tilemap[door_s + self.PATH_S] is self.EMOJI['WOODS']:
                #         self.tilemap[door_s] = self.EMOJI['DOOR']
                #     if self.tilemap[door_e + self.PATH_E] is self.EMOJI['WOODS']:
                #         self.tilemap[door_e] = self.EMOJI['DOOR']
                #     if self.tilemap[door_w + self.PATH_W] is self.EMOJI['WOODS']:
                #         self.tilemap[door_w] = self.EMOJI['DOOR']

    def makeCamp(self):
        '''Function to populate array randomly'''

        tile_data = [
            (MapData.EMOJI['WOODS'], 40),
            (MapData.EMOJI['CABIN'], 0.5),
            (MapData.EMOJI['WATER'], 0.5),
            (MapData.EMOJI['FIELD'], 10),
            (MapData.EMOJI['TREE'], 5),
            (MapData.EMOJI['ROCK'], 0.1),
        ]

        for index in range(self.GAMESIZE * self.GAMESIZE):

            # set edge tiles
            if self.isEdgeIndex(index):
                self.tilemap.append(MapData.EMOJI['TREE'])
                continue

            # randi = random.randint(0, 999)

            # if randi <= 1:
            #     tile_type = MapData.EMOJI['WATER']
            # elif 2 <= randi <= 875:
            #     tile_type = MapData.EMOJI['WOODS']
            # elif 876 <= randi <= 899:
            #     tile_type = MapData.EMOJI['FIELD']
            # elif 900 <= randi <= 989:
            #     tile_type = MapData.EMOJI['TREE']
            # elif 990 <= randi <= 999:
            #     tile_type = MapData.EMOJI['CABIN']

            # generate tile
            tile_type, _ = random.choices(
                tile_data, weights=[weight for _, weight in tile_data], k=1)[0]

            # add tile to tile list
            self.tilemap.append(tile_type)

            # save tile to list by type
            if tile_type == MapData.EMOJI['CABIN']:
                self.tilelist_cabin.append(index)
            if tile_type == MapData.EMOJI['WATER']:
                self.tilelist_water.append(index)

    def makeCabin(self):
        '''Function to expand cabin tiles randomly'''

        deep = 3 + random.randint(0, self.EDGESIZE // 2)
        wide = 3 + random.randint(0, self.EDGESIZE // 2)

        for index in self.tilelist_cabin:

            # chance to make monument instead
            if random.randint(0, 9) == 0:
                self.populateMonuments(Monuments.someMonument(), index)
                return

            # generate size
            self.drawRect(index=index, deep=deep, wide=wide,
                          value=MapData.EMOJI['CABIN'])
            # add doors
            self.makeDoor(tall=deep, wide=wide)

            # add traps

            # Use enumerate to get index and tile
            for index, tile in enumerate(self.tilemap):
                if tile == MapData.EMOJI['CABIN']:
                    chance = random.randint(0, 94)
                    if chance == 0:
                        self.tilemap[index] = MapData.EMOJI['WRECKED']

    def makeSafeSpawn(self):
        """Function to ensure safe spawn point"""
        self.drawRectOmni(
            index=self.GRID_SW,
            wide=4,
            deep=4,
            value=MapData.EMOJI['CABIN'],
            direction="upright"
        )

    @ property
    def randomIndex(self):
        while True:
            random_index = random.randint(0, self.GAMESIZE * self.GAMESIZE - 1)
            if self.tilemap[random_index] == MapData.EMOJI['WOODS']:
                return random_index

    def __init__(self, GAMESIZE, EDGESIZE):
        '''Make game map'''

        # save instances
        MapData.all_calls += 1
        MapData.all_instances.append(self)

        # instace vars
        self.GAMESIZE = GAMESIZE
        self.EDGESIZE = EDGESIZE

        # tile lists
        self.tilemap = []
        self.tilelist_cabin = []
        self.tilelist_water = []
        self.tilelist_woods = []

        self.all_shapes = []

        self.tilelist_block = ()

        # grid tile positions
        self.GRID_NE = EDGESIZE * GAMESIZE - EDGESIZE + GAMESIZE - 1
        self.GRID_NW = GAMESIZE * EDGESIZE + EDGESIZE
        self.GRID_SE = GAMESIZE * GAMESIZE - EDGESIZE * GAMESIZE - EDGESIZE - 1
        self.GRID_SW = GAMESIZE * GAMESIZE - EDGESIZE * GAMESIZE + EDGESIZE - GAMESIZE

        # directional offsets
        self.PATH_N = -GAMESIZE
        self.PATH_S = GAMESIZE
        self.PATH_E = 1
        self.PATH_W = -1
        self.PATH_NE = -GAMESIZE + 1
        self.PATH_NW = -GAMESIZE - 1
        self.PATH_SE = GAMESIZE + 1
        self.PATH_SW = GAMESIZE - 1

        # directional groups
        self.COMPASS_8 = [self.PATH_N,
                          self.PATH_S,
                          self.PATH_E,
                          self.PATH_W,
                          self.PATH_NW,
                          self.PATH_NE,
                          self.PATH_SW,
                          self.PATH_SE]
        self.COMPASS_4 = [self.PATH_N,
                          self.PATH_S,
                          self.PATH_E,
                          self.PATH_W]
        self.COMPASS_X = [self.PATH_NW,
                          self.PATH_NE,
                          self.PATH_SW,
                          self.PATH_SE]

        # make tile map iteratively
        self.makeCamp()
        self.populateShapes()
        self.makeSafeSpawn()

        # make some tiles manually
        self.tilemap[self.GRID_NE] = MapData.EMOJI['SAVED']
        self.tilemap[self.GRID_NW] = MapData.EMOJI['WRECKED']

        # make some tiles manually - add doors to safe spawn
        self.tilemap[self.GRID_SW + 3] = MapData.EMOJI['DOOR']
        self.tilemap[self.GRID_SW - (GAMESIZE * 3)] = MapData.EMOJI['DOOR']

        # save map to disk
        self.exportTextFile()
