'''Module for moving AI entity definition'''

import random
from datetime import datetime

from m_tiles import *
from m_icons import *


# ENTITY META CLASS
# ------------------------------------------------------------------------------


class UnitsMeta(type):
    """
    Metaclass for creating Tile subclasses with shared properties.
    """

    def __init__(cls, name, bases, attrs):
        super().__init__(name, bases, attrs)
        cls.all_calls = 0
        cls.all_insts = []
        cls.live_insts = []
        cls.past_insts = []

    def __call__(cls, *args, **kwargs):
        '''This method is called when an instance of the class is created.'''
        instance = super().__call__(*args, **kwargs)
        cls.all_calls += 1
        cls.all_insts.append(instance)
        return instance

    @classmethod
    def getEachInst(mcs, base_class):  # Use mcs instead of cls
        '''Function to show subclasses and instances'''

        data = {}  # Use a dictionary instead of a list
        for cls in base_class.__subclasses__():
            data[cls.__name__] = cls.all_calls  # Key-value pairs
        return data


# ENTITY CLASS
# ------------------------------------------------------------------------------


class Units(metaclass=UnitsMeta):

    """Class to manage all non-human entities"""

    def __init__(self):

        # save instance data
        Units.all_calls += 1
        Units.all_insts.append(self)

        # varse
        # self.lifetime = datetime.now()

        self.view_size = 9  # grid size of draw on spectate
        self.VIEW_RADI = (self.view_size - 1) // 2
        self.uniqueid = Units.all_calls

        # vars - movement
        self.travellog = set()
        self.move_history = []

        # vars - movement - tile step
        self.last_tile = None
        self.this_tile = None

        # vars - movement - data
        self.move_fail = 0  # to invalid tile
        self.move_pass = 0  # to valid tile
        self.move_hits = 0  # to enemy tile (kills)
        self.move_numb = 0  # move total
        self.move_skip = 0  # turn w/o movement for teleport
        self.move_tile_max = 0  # total accessible tiles

        # vars - combat
        # self.points_at = 0
        # self.points_df = 0
        # self.points_hp = 10
        # self.points_xp = 0
        # self.points_max_hp = 10

        # init dynamic attributes
        self.move_rate = self.setMoveRate()  # move delay

    def factory(self, ClassName, number):

        for _ in range(number):
            new_entity = ClassName()

    @property
    def possibleTiles(self):
        '''Function to count all entity-accessible tiles'''

        # only calc once
        if self.move_tile_max == 0:
            for tile in Tiles.all_insts:

                # no edge tiles
                if not tile.tile_edge:

                    # only passable tiles
                    if tile.__class__ in self.PASS_LIST:
                        self.move_tile_max += 1

        return self.move_tile_max

    @property
    def isLiving(self):
        if self.points_hp > 0:
            return True

    @property
    def lifeTime(self):
        lifetime = datetime.now() - self.lifetime
        lifetime = lifetime.strftime("%y%m%d %H:%M:%S.%f")
        return lifetime

    @property
    def moveRate(self):
        if self.move_numb == 0:
            return "0%"
        else:
            percentage = 1 - (self.move_fail / self.move_numb)
            percentage = int(percentage * 100)
            return str(percentage) + "%"

    @property
    def mapCoverage(self):
        """Function to get unique indexs."""
        coverage = len(self.travellog)
        return coverage

    def setMoveRate(self):
        '''Function to randomly generate move rate'''
        min = self.move_rate_min
        max = self.move_rate_max
        move_rate = round(random.uniform(min, max), 2)
        return move_rate

    def takeDamage(self, damage):

        damage = damage - self.points_df
        self.points_hp = self.points_hp - damage


# ENTITY SUB CLASSES
# ------------------------------------------------------------------------------

class KnifeEntity(Units):

    def __init__(self):

        self.home = WoodsTile
        self.icon = EMOJI['KNIFE']
        self.name = 'knife'
        self.move_rate_min = .2
        self.move_rate_max = .8
        self.move_type = 'idle'
        self.PASS_LIST = [
            DoorsTile,
            FieldsTile,
            TreesTile,
            WoodsTile,
        ]

        super().__init__()


class SnakeEntity(Units):

    def __init__(self):

        self.home = RocksTile
        self.icon = EMOJI['SNAKE']
        self.move_rate_min = .5
        self.move_rate_max = 3
        self.move_type = 'idle'
        self.PASS_LIST = [
            FieldsTile,
            RocksTile,
            TreesTile,
            WoodsTile,
            WrecksTile,
        ]

        super().__init__()


class SpiderEntity(Units):

    def __init__(self):

        self.home = CabinsTile
        self.icon = EMOJI['SPIDER']
        self.move_rate_min = 5
        self.move_rate_max = 60
        self.move_type = 'idle'
        self.PASS_LIST = [
            CabinsTile,
            DoorsTile,
        ]

        super().__init__()


class WolfEntity(Units):

    def __init__(self):

        self.home = WoodsTile
        self.icon = EMOJI['WOLF']
        self.move_rate_min = .5
        self.move_rate_max = 2
        self.move_type = 'idle'
        self.PASS_LIST = [
            FieldsTile,
            WoodsTile,
        ]

        super().__init__()
