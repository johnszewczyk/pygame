import random
from datetime import datetime


def TSTAMP():
    now = datetime.now()
    now = now.strftime("%y%m%d %H:%M:%S.%f")
    now = now[:18]
    return now


class UserData:
    """Class to manage all human users; Inst by new network conns"""

    log = []
    all_calls = 0
    all_insts = []

    EMOJI = [

        # Running Emojis
        '🏃🏿‍♀️', '🏃🏿‍♂️', '🏃🏿',
        '🏃🏾‍♀️', '🏃🏾‍♂️', '🏃🏾',
        '🏃🏽‍♀️', '🏃🏽‍♂️', '🏃🏽',
        '🏃🏼‍♀️', '🏃🏼‍♂️', '🏃🏼',
        '🏃🏻‍♀️', '🏃🏻‍♂️', '🏃🏻',
        '🏃‍♀️', '🏃‍♂️', '🏃',

        # Wheelchair Emojis
        '👩🏿‍🦽', '👨🏿‍🦽', '🧑🏿‍🦽',
        '👩🏾‍🦽', '👨🏾‍🦽', '🧑🏾‍🦽',
        '👩🏽‍🦽', '👨🏽‍🦽', '🧑🏽‍🦽',
        '👩🏼‍🦽', '👨🏼‍🦽', '🧑🏼‍🦽',
        '👩🏻‍🦽', '👨🏻‍🦽', '🧑🏻‍🦽',
        '👩‍🦽', '👨‍🦽', '🧑‍🦽'
    ]

    def __init__(self, addr, conn):

        # uses
        UserData.all_calls += 1
        UserData.all_insts.append(self)

        # save args
        self.icon = self.pickIcon()
        self.addr = addr
        self.conn = conn

        # vars
        self.user_numb = UserData.all_calls
        self.time = datetime.now()

        # vars - movement
        self.last_tile = None
        self.this_tile = None

        self.view_size = 9  # distance a player can see/ client grid size
        self.VIEW_RADI = (self.view_size - 1) // 2

        # vars - play history
        self.life_numb = 0
        self.loss_numb = 0
        self.loss_tile = []
        self.loss_time = []

        # vars - move history
        self.move_numb = 0
        self.move_pass = 0
        self.move_fail = 0
        self.move_history = []
        self.travellog = set()

        # vars - combat
        # self.points_at = 0
        # self.points_df = 0
        # self.points_hp = 2
        # self.points_xp = 0
        # self.points_max_hp = 2

        # make entry
        namedata = f"""{self.conn} {self.icon} {self.user_numb}"""
        print(f"""{TSTAMP()} [cls.play] {namedata}: NEW PLAYER""")

        log = f"""{TSTAMP()} [cls.play] {namedata}: NEW PLAYER"""
        UserData.clsLog(log)

    @classmethod
    def clsLog(cls, string: str):
        """Class function to timestamp and save notifications."""

        string = str(TSTAMP() + " " + string)
        cls.log.append(string)

    @classmethod
    def listAllPlayers(cls):
        print("LIST ALL PLAYERS")
        for player in UserData.all_insts:
            time_online = datetime.now() - player.time
            print(
                " ",
                player.conn,
                player.icon,
                "@",
                player.position,
                time_online
            )

    @classmethod
    def listPlayerPositions(cls):
        """Returns a list of all player positions."""
        return [player.position for player in cls.all_insts]

    @classmethod
    def getNearestPlayer(cls, index):
        """Return player nearest to [index]"""

        nearest_player = None

        # if there are no players, skip
        if len(UserData.all_insts) == 0:
            return None

        min_distance = float('inf')

        for player in cls.all_insts:
            distance = abs(player.position - index)
            if distance < min_distance:
                min_distance = distance
                nearest_player = player
        if nearest_player:
            return nearest_player.position

        return None

    @classmethod
    def pickIcon(cls):
        icon = random.choice(cls.EMOJI)
        return icon

    @property
    def getTimeOnline(self):
        duration = datetime.now() - self.time
        # Convert timedelta to total seconds and then format
        total_seconds = duration.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    @property
    def isLiving(self):
        if self.points_hp > 0:
            return True

    def recordLoss(self):
        """Function to save loss data upon loss"""
        time = datetime.now()
        self.life_numb += 1
        self.loss_numb += 1
        self.loss_tile.append(self.this_tile)
        self.loss_time.append(time)

        # log
        log = f"""{self.icon} {self.user_numb} lost after {
            time - self.time} and {self.move_numb} moves"""
        UserData.clsLog(log)
