import random
from datetime import datetime, timedelta


class PlayerData:
    """Class to manage all human users; Inst by new network conns"""

    all_calls = 0
    all_instances = []

    EMOJI = [
        '🏃🏿‍♀️', '🏃🏿‍♂️', '🏃🏿',
        '🏃🏾‍♀️', '🏃🏾‍♂️', '🏃🏾',
        '🏃🏽‍♀️', '🏃🏽‍♂️', '🏃🏽',
        '🏃🏼‍♀️', '🏃🏼‍♂️', '🏃🏼',
        '🏃🏻‍♀️', '🏃🏻‍♂️', '🏃🏻',
        '🏃‍♀️', '🏃‍♂️', '🏃',
    ]
    ICON = {}
    ICON['COFFIN'] = '⚰️'

    def __init__(self, addr, conn):

        # save all instances
        PlayerData.all_calls += 1
        PlayerData.all_instances.append(self)

        # save args
        self.icon = self.pickIcon()
        self.addr = addr
        self.conn = conn
        self.time = datetime.now()

        # move vars
        self.position = None
        self.last_pos = None

        # keep track of data
        self.loss_numb = 0
        self.loss_area = []
        self.loss_time = []
        self.move_numb = 0

        # notify
        print(self.time,  self.conn, "[PlayerData] new player", self.all_calls)

    @classmethod
    def listAllPlayers(cls):
        print("LIST ALL PLAYERS")
        for player in PlayerData.all_instances:
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
        return [player.position for player in cls.all_instances]

    @classmethod
    def getNearestPlayer(cls, index):
        """Return player nearest to [index]"""

        # if there are no players, skip
        if len(PlayerData.all_instances) == 0:
            return 1

        nearest_player = None
        min_distance = float('inf')

        for player in cls.all_instances:
            distance = abs(player.position - index)
            if distance < min_distance:
                min_distance = distance
                nearest_player = player
        if nearest_player:
            # print("NEAREST IS :", nearest_player.position)
            return nearest_player.position

    @classmethod
    def pickIcon(cls):
        icon = random.choice(cls.EMOJI)
        return icon

    def getTimeOnline(self):
        duration = datetime.now() - self.time
        # Convert timedelta to total seconds and then format
        total_seconds = duration.total_seconds()
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"

    def recordLoss(self):
        """Function to save loss data upon loss"""
        self.loss_numb += 1
        self.loss_area.append(self.position)
        self.loss_time.append(datetime.now())
