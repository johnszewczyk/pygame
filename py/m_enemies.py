import random
from datetime import datetime


class EntityData:

    """Class to manage all non-human entities"""

    EMOJI = {}
    EMOJI["KNIFE"] = "🔪"
    EMOJI["WOLF"] = "🐺"
    EMOJI["SPIDER"] = "🕷️"

    all_calls = 0
    all_insts = []

    def __init__(self, UNIT_ICON, MOVE_TYPE, HOME_TILE):

        # save instance data
        EntityData.all_calls += 1
        EntityData.all_insts.append(self)

        # args - constants
        self.UNIT_ICON = UNIT_ICON
        self.HOME_TILE = HOME_TILE
        self.MOVE_TYPE = MOVE_TYPE

        # vars
        # self.lifetime = datetime.now()
        self.position = 0
        self.lastposi = 0
        self.viewsize = 9  # grid size of draw on spectate; unused
        self.viewradi = (self.viewsize - 1) // 2
        self.uniqueid = EntityData.all_calls

        # vars - movement
        self.travellog = {}
        self.last_posi = self.position
        self.move_fail = 0  # to invalid tile
        self.move_succ = 0  # to valid tile
        self.move_hits = 0  # to enemy tile (kills)
        self.move_numb = 0  # move total
        self.move_rate = round(random.uniform(0.25, 1.25), 2)  # move delay
        self.move_skip = 0  # turn w/o movement for teleport

        # vars - combat
        self.points_at = 0
        self.points_df = 0
        self.points_hp = 10
        self.points_xp = 0
        self.points_max_hp = 10

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

    @staticmethod
    def factory(quantity, UNIT_ICON, MOVE_TYPE, HOME_TILE):
        for i in range(quantity):
            inst = EntityData(
                UNIT_ICON=UNIT_ICON,
                MOVE_TYPE=MOVE_TYPE,
                HOME_TILE=HOME_TILE,
            )

    @classmethod
    def getEntityIndices(cls):
        """Return all entity location indices"""
        return (entity.position for entity in cls.all_insts)

    def takeDamage(self, damage):

        damage = damage - self.points_df
        self.points_hp = self.points_hp - damage
