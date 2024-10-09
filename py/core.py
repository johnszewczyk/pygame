#!/usr/bin/python3
'''Core Module for tile game

TO DO
  - Safe spawn
  - Exit tile
  - Flip draw
  - Prgm data page
  - User data page
  - Data-by-request
  - Sort data
  - Data sub page


'''


# game modules
from m_icons import *
from m_maps import *
from m_users import *
from m_units import *

# standard imports
import asyncio
import certifi  # to enable SSL connections
import copy
import json  # to send data to web interface
import os  # to clear terminal
import platform  # to report hardware to web interface
import psutil  # to report system to web interface
import random
import ssl  # to enable SSL connections
import sys
import time
import websockets

from datetime import datetime, timedelta


class SuperMeta(type):
    '''Metaclass to document subclasses and functions'''
    class_data = []

    def __new__(cls, name, bases, dct):
        class_info = {
            'name': name,
            'bases': [base.__name__ for base in bases],
            'docstring': dct.get('__doc__', ''),
            'methods': [],
            'attributes': []
        }

        for key, value in dct.items():
            if callable(value):
                method_info = {
                    'name': key,
                    'docstring': value.__doc__
                    # Removed 'code': inspect.getsource(value)
                }
                class_info['methods'].append(method_info)
            elif not key.startswith('__'):
                attribute_info = {
                    'name': key
                    # Removed 'value': value
                }
                class_info['attributes'].append(attribute_info)

        SuperMeta.class_data.append(class_info)

        return super().__new__(cls, name, bases, dct)

    @classmethod
    def print_info(cls):
        """Prints the collected class information."""
        for class_info in cls.class_data:
            print(f"Class: {class_info['name']}")
            print(f"  Docstring: {class_info['docstring']}")
            print("  Bases:", class_info['bases'])

            for method in class_info['methods']:
                print(f"    Method: {method['name']}")
                print(f"      Docstring: {method['docstring']}")

            for attribute in class_info['attributes']:
                print(f"    Attribute: {attribute['name']}")


# HELP FUNC
# ------------------------------------------------------------------------------


def clear():
    '''Function to clear terminal'''
    os.system("cls" if os.name == "nt" else "clear")


def monitor_server_load():
    process = psutil.Process()  # Get current process info
    cpu_percent = process.cpu_percent()
    memory_info = process.memory_info()
    rss_memory_mb = memory_info.rss / (1024 ** 2)  # Calculate in MB
    rss_memory_mb = int(rss_memory_mb)  # Convert to integer

    return cpu_percent, rss_memory_mb


def TSTAMP():
    now = datetime.now()
    now = now.strftime("%y%m%d %H:%M:%S")
    now = now[:18]
    return now


# GAME CORE
# ------------------------------------------------------------------------------

class ArenaData:

    log = []

    def __init__(self) -> None:
        pass

    @classmethod
    def battMode(cls, aggressor, defender):
        cls.log.append(datetime.now())

        while aggressor.points_hp > 0 or defender.points_hp > 0:
            print("COMBAT ROUND")

            # defender gets first strike; i.e., never the user
            aggressor.takeDamage(defender.points_at)
            defender.takeDamage(aggressor.points.at)

            if aggressor.isLiving:
                return True
            else:
                return False


class GameData(metaclass=SuperMeta):
    '''Class to hold data for level design, statistic operations, globals'''

    # game_size: must be perfect square.
    # view_size: must be odd and <= (2 * view_size - 1)

    # GLOBAL - map data
    view_size = 9
    edge_size = view_size // 2 + 1
    game_size = None

    # stage number
    game_zone = 0

    # game time and stage time
    game_time = datetime.now()
    zone_time = datetime.now()

    BOARDS = {
        # need zero place for first loop
        0: 0,
        1: 36,
        2: 64,
        3: 100,
        4: 144,
        5: 196,
        6: 256,
        7: 324,
        8: 400,
        9: 484,
        10: 576,
    }

    @classmethod
    def stageTime(cls):
        elapsed_time = datetime.now() - cls.zone_time
        # Format elapsed time as HH:MM:SS
        return str(timedelta(seconds=elapsed_time.seconds))

    @classmethod
    def lastStage(cls):
        '''Function to load last/ previous stage'''
        if cls.game_zone > 0:
            cls.game_zone -= 1
            cls.zone_time = datetime.now()
            cls.game_size = cls.BOARDS[cls.game_zone]

    @classmethod
    def nextStage(cls):
        '''Function to load next/ upcoming stage'''
        if cls.game_zone < len(cls.BOARDS) - 1:
            cls.game_zone += 1
            cls.zone_time = datetime.now()
            cls.game_size = cls.BOARDS[cls.game_zone]

    @classmethod
    def gameTime(cls):
        elapsed_time = datetime.now() - cls.game_time
        # Format elapsed time as HH:MM:SS
        return str(timedelta(seconds=elapsed_time.seconds))

    @classmethod
    def zoneTime(cls):
        elapsed_time = datetime.now() - cls.zone_time
        # Format elapsed time as HH:MM:SS
        return str(timedelta(seconds=elapsed_time.seconds))


class UnitPool(metaclass=SuperMeta):
    '''Class to hold spawn templates.'''

    @staticmethod
    def autoPopulate():
        '''Function to make entities based on map size'''

        # wipe all
        Units.all_insts = []

        # unit rates
        unit_distribution = [
            (KnifeEntity, GameData.game_size // 36),
            (SnakeEntity, RocksTile.all_calls // 4),
            (SpiderEntity, CabinsTile.all_calls // 12),
            (WolfEntity, GameData.game_size // 4),
        ]

        # make inst
        for unit_class, quantity in unit_distribution:
            for _ in range(quantity):
                unit_class()  # Create an instance of the unit class

    @staticmethod
    def spawnPlayer(user):
        '''Function to put user at starting index'''

        # calc map middle, for now
        map_middle = (GameData.game_size *
                      GameData.game_size) // 2 + (GameData.game_size // 2)

        middle_tile = Tiles.all_insts[map_middle]

        # set user position
        user.last_tile = middle_tile
        user.this_tile = middle_tile

        GameCore.clsLog(f'''{user.icon} {user.user_numb}: spawns.''')

    @staticmethod
    def spawnAll():
        '''Function to place all units at random valid index'''

        for unit in Units.all_insts:

            # save unit location
            unit.this_tile = GameCore.randomIndexType(unit)

            # save move data
            GateKeeper.saveMoveData(unit, unit.this_tile)

        print(f"{TSTAMP()} spawned all units")

    @staticmethod
    def spawnOne(unit):
        '''Function to place a unit at random valid index'''

        # save unit location
        unit.this_tile = GameCore.randomIndexType(unit)

        # save move data
        GateKeeper.saveMoveData(unit, unit.this_tile)


class GateKeeper(metaclass=SuperMeta):
    '''Class to validate unit movement'''

    uses = 0

    def __init__(self) -> None:
        GateKeeper.uses += 1

    @staticmethod
    def gatekeep(tile, unit):
        '''Function to validate unit movement to next tile'''

        # if tile is NOT edge-type...
        if not tile.tile_edge:
            # if tile is passable by unit...
            if tile.__class__ in unit.PASS_LIST:

                # save move
                GateKeeper.saveMoveData(unit, tile)
                return True
        else:
            # deny move
            unit.move_fail += 1
            return False

    @staticmethod
    def saveMoveData(unit, tile):
        '''Function to finalize a movement, updating tile and unit datas'''

        GateKeeper

        def updateTileData(unit, tile):
            '''Function to save tile data upon movement'''

            # add unit to tile
            tile.this_tile = unit

            # save tile uses
            tile.tile_uses.append(datetime.now())

            # save last visitor's icon
            tile.tile_last_user = f"{unit.icon}"

            # save each visitor's instance - unique only
            tile.tile_user_list.add(unit)

            # save each visitor's icon - unique only
            tile.tile_user_icon.add(unit.icon)

        def updateUnitData(unit, next_tile):
            '''Function to save unit data upon movement'''

            # save unit tile data
            unit.last_tile = unit.this_tile
            unit.this_tile = next_tile

            # save unit move data
            unit.move_pass += 1
            unit.move_history.append(unit.this_tile)
            unit.travellog.add(unit.this_tile)

        updateUnitData(unit, tile)
        updateTileData(unit, tile)


class GameCore(metaclass=SuperMeta):
    '''Class to hold all gameplay logic elements.'''

    log = []

    def __init__(self) -> None:

        self.nextGame()

    @staticmethod
    def randomIndexType(unit):
        '''Function to pick random valid index.'''

        # Get all valid tiles for the unit
        valid_tiles = []
        for tile in Tiles.all_insts:
            if tile.tile_access and tile.__class__ in unit.PASS_LIST:
                valid_tiles.append(tile)

        # Choose a random tile from the valid tiles
        return random.choice(valid_tiles)

    @staticmethod
    def getIndexfromXY(x, y):
        '''Function to convert from X,Y to POSITION'''
        index = y * GameData.game_size + x
        return index

    @staticmethod
    def getXYFromIndex(index):
        '''Function to convert from POSITION to X,Y'''
        x = index % GameData.game_size
        y = index // GameData.game_size
        return x, y

    @classmethod
    def clsLog(cls, string: str):
        '''Class function to timestamp and save notifications.'''
        string = f'''{TSTAMP()} {cls.__name__} {string}'''
        cls.log.append(string)

    @classmethod
    def shutdown(cls):
        '''Function to force quit.'''
        sys.exit(0)

    # GAME OPERATIONS

    @staticmethod
    def moveUnitIdle(unit):
        '''Primary movement method; one tile NSEW'''

        # init move; save last tile
        unit.move_numb += 1
        unit.last_tile = unit.this_tile

        # pick path
        next_move = random.randint(0, 3)

        # base - current position
        new_offset = unit.this_tile.tile_index

        # base + path movement
        if next_move == 0:
            new_offset += 1
        if next_move == 1:
            new_offset -= 1
        if next_move == 2:
            new_offset += GameData.game_size
        if next_move == 3:
            new_offset -= GameData.game_size

        # save next tile
        next_tile = Tiles.all_insts[new_offset]

        # VALIDATE MOVEMENT

        if GateKeeper.gatekeep(next_tile, unit):
            return True
        else:
            # deny move
            unit.move_fail += 1
            return False

    def moveEntityHunt(self, unit):
        '''
        Function to move ARG1 [unit] @ target index.
        Entities hunting effectively take two turns thus moving diagonally.
        '''

        # find nearest target index
        target_index = UserData.getNearestPlayer(unit.this_tile)

        if target_index == None:
            # console log
            # print(f"{TSTAMP()} GameCore: moveEntityHunt: no target")
            GameCore.moveUnitIdle(unit)
            return

         # save tile at target index
        target_tile = Tiles.all_insts[target_index]

        # console log
        # print(f'''{TSTAMP} GameCore: moveEntityHunt {target_index}''')

        # save last/current tile
        unit.last_tile = unit.this_tile

        # move at target
        unit.move_numb += 1

        # convert indices to x,y for comparison
        unit_x, unit_y = self.getXYFromIndex(unit.this_tile)

        # unit horizontal movement
        if unit_x < target_tile.tile_posx:
            unit_x += 1
        if unit_x > target_tile.tile_posx:
            unit_x -= 1

        # make new index from x,y
        new_index = self.getIndexfromXY(unit_x, unit_y)

        # check tile - approve
        if Tiles.all_insts[new_index].__class__ in unit.PASS_LIST:
            unit.this_tile = new_index
            unit.move_pass += 1

        # convert indices to x,y for comparison
        unit_x, unit_y = self.getXYFromIndex(unit.this_tile)

        # unit vertical movement
        if unit_y < target_tile.tile_posy:
            unit_y += 1
        if unit_y > target_tile.tile_posy:
            unit_y -= 1

        # make new index
        new_index = self.getIndexfromXY(unit_x, unit_y)

        # check tile - approve
        if Tiles.all_insts[new_index].__class__ in unit.PASS_LIST:
            unit.this_tile = new_index
            unit.move_pass += 1

        # teleport if stuck after X turns // 2
        if unit.this_tile == unit.last_tile:
            unit.move_skip += 1
            if unit.move_skip == 6:
                unit.move_skip = 0
                unit.this_tile = self.randomIndexType(unit)
                return

    @staticmethod
    def movePlayer(user, user_input):
        '''Function to process user hardware input to action'''

        print("move player")

        # placeholder
        new_offset = 0

        if user_input == "w":
            new_offset = -GameData.game_size
        elif user_input == "s":
            new_offset = GameData.game_size
        elif user_input == "a":
            new_offset = -1
        elif user_input == "d":
            new_offset = 1

        # readability: get user's occupied tile type & next tile type
        this_tile = user.this_tile
        next_tile = Tiles.all_insts[user.this_tile.tile_index + new_offset]

        # is tile passable
        if not next_tile.tile_access:
            print('tile not passable')
            return 1

        # block cabins - entry - also allow entry to traps with roofs
        if next_tile.tile_roof and not next_tile.tile_trap:
            if not this_tile.__class__ in next_tile.tile_link:
                print('tile is roof/ wall')
                return 1

        # block cabins - exit
        if this_tile.tile_roof:
            if not next_tile.tile_roof:
                if next_tile.__class__ not in this_tile.tile_link:
                    print('tile is not related')
                    return 1

        # block users by index
        for some_user in UserData.all_insts:
            if user is not some_user:
                if user.this_tile == some_user.this_tile:
                    return 1

        # save move data
        GateKeeper.saveMoveData(user, next_tile)
        GameCore.clsLog(f'''{user.icon} {user.user_numb}: move #{
            user.move_numb}''')

    # GAME STATES

    def gameOver(self):
        '''Function to check for user loss or level complete.'''

        for user in UserData.all_insts:

            # did user hit loss tile
            if user.this_tile.tile_trap:
                print(user.icon, user.this_tile.tile_trap_text)

                GameCore.clsLog(
                    f'''{user.icon} {user.user_numb}
                        {user.this_tile.tile_trap_text}'''
                )

                user.recordLoss()
                UnitPool.spawnPlayer(user)

            # did user hit exit
            if user.this_tile.tile_exit:
                GameCore.nextGame()
                GameCore.clsLog(f'''{user.icon} wins!''')

            # did user hit enemy
            for unit in Units.all_insts:
                if user.this_tile == unit.this_tile:

                    # FIGHT

                    # if not ArenaData.battMode(user, unit):

                    user.recordLoss()
                    unit.move_hits += 1
                    UnitPool.spawnOne(unit)
                    UnitPool.spawnPlayer(user)

                    # log
                    print(TSTAMP(), "[cls.game]", user.conn,
                          "hits", unit.icon, "#", user.loss_numb)
                    GameCore.clsLog(
                        f'''{unit.icon} > {user.icon} {user.user_numb}: #{user.loss_numb}''')

    @staticmethod
    def nextGame():
        '''Function to make new game while network is active.'''

        print(f'{TSTAMP()} next game')

        # increment stage
        GameData.nextStage()

        # make world
        tileland = TileLand(
            GameData.game_size,
            GameData.edge_size,
        )

        # make users
        for user in UserData.all_insts:
            UnitPool.spawnPlayer(user)

        # make enemies; init enemies
        UnitPool.autoPopulate()
        UnitPool.spawnAll()

    async def gameLoop(self):
        '''Coroutine to execute main game loop logic'''

        last_move_times = {}

        while True:

            # MOVE ENTITIES

            current_time = datetime.now()
            for unit in Units.all_insts:
                if unit not in last_move_times:
                    # Initialize last move time
                    last_move_times[unit] = current_time

                time_since_last_move = current_time - last_move_times[unit]
                if time_since_last_move.total_seconds() >= unit.move_rate:
                    if unit.move_type == "idle":
                        GameCore.moveUnitIdle(unit)
                    if unit.move_type == "hunt":
                        GameCore.moveEntityHunt(unit)
                    # Update last move time
                    last_move_times[unit] = current_time

            # is game over
            self.gameOver()

            # game loop speed
            await asyncio.sleep(0.02)


class ViewData(metaclass=SuperMeta):
    '''Class to make user view grid.'''

    @staticmethod
    def makeFullView():
        '''Function to make complete tile grid view'''

        # brute-force regen of framebuffer
        framebuffer = []
        for tile in Tiles.all_insts:
            framebuffer.append(tile.tile_icon)

        # add users to framebuffer
        for user in UserData.all_insts:

            # add headstones to framebuffer
            for tile in user.loss_tile:
                framebuffer[tile.tile_index] = EMOJI["GRAVE"]

            # add user after headstone (z-position logic)
            framebuffer[user.this_tile.tile_index] = user.icon

        # add enemies to framebuffer
        for unit in Units.all_insts:
            framebuffer[unit.this_tile.tile_index] = unit.icon

        return framebuffer

    @staticmethod
    def makeUserView(user):
        '''Function to make a small range of the map centered on an index.
        Returns a square array of [user's view radius]-size for a given user.
        Uses grid logic; for each row, for each col, check tile.'''

        # save user tile inst
        user_tile = user.this_tile

        # calc view dist
        lower_bound = user.VIEW_RADI * -1
        offsets = []
        output = []

        # make range
        for i in range(user.view_size):
            offsets.append(lower_bound)
            lower_bound += 1

        # for each tile in grid
        for yoff in offsets:
            for xoff in offsets:
                # increment columns rows
                new_offset = xoff + \
                    (yoff * GameData.game_size) + \
                    user.this_tile.tile_index

                # Z-INDEX LOGIC / STACK BASE ICON

                # 1. get tile object
                tile_to_draw = Tiles.all_insts[new_offset]

                # 2. get base icon
                drawthis = tile_to_draw.tile_icon

                # 3. add alt. (from interior view) icon if...
                if user_tile.tile_roof:
                    if tile_to_draw.tile_icon_from_interior:
                        drawthis = tile_to_draw.tile_icon_from_interior

                # Z-INDEX LOGIC / STACK ENTITIES

                # 5. add unit - LAZY LOOP
                for unit in Units.all_insts:

                    # if unit on tile-to-draw...
                    if tile_to_draw == unit.this_tile:

                        # if user outside...
                        if not user_tile.tile_roof:
                            # if unit tile outside...
                            if not tile_to_draw.tile_roof:
                                # draw unit
                                drawthis = unit.icon

                        # if user inside...
                        if user_tile.tile_roof:
                            # if unit tile inside...
                            if tile_to_draw.tile_roof:
                                # draw unit
                                drawthis = unit.icon

                # Z-INDEX LOGIC / STACK PLAYERS

                # 6. add users
                for user in UserData.all_insts:
                    if tile_to_draw == user.this_tile:
                        drawthis = user.icon

                # save to list for send to client
                output.append(drawthis)
        return output


# NETWORK
# ------------------------------------------------------------------------------


class AdminServer(metaclass=SuperMeta):
    '''Server object to send data to HTML interface.'''

    userlist = set()

    def __init__(self, ADDR, PORT) -> None:
        self.ADDR = ADDR
        self.PORT = PORT
        self.server = None

        # MAKE TILE TYPE FILTER

        # list all defined tile types
        self.tile_types = Tiles.__subclasses__()
        self.enabled_tile_types = set()

        # enable a tile type by default
        self.enabled_tile_types.add(WoodsTile.__name__)

        # report
        print(f"{TSTAMP()} ADMIN SERVER UP: {self.ADDR}:{self.PORT}")

    async def handle_connection(self, websocket, path):
        '''Handles incoming connections from admin clients and sends updates.'''

        # connection
        AdminServer.userlist.add(websocket.remote_address)
        print(f'''{TSTAMP()} {self.__class__.__name__} {
            websocket.remote_address} connected''')

        while True:
            try:
                # datas to send
                await self.sendUnitData(websocket)
                await self.sendUnitView(websocket)
                await self.sendFullView(websocket)
                await self.sendGameData(websocket)
                await self.sendLogData(websocket)
                await self.sendNetData(websocket)
                await self.sendUserData(websocket)
                await self.sendPrgmData(websocket)
                await self.sendServerData(websocket)
                await self.sendTileData(websocket)

                try:
                    # datas to receive; set timeout as needed
                    message = await asyncio.wait_for(websocket.recv(), timeout=0.1)

                    # RECEIVE: new game button
                    data = json.loads(message)
                    if data["type"] == "new_game_request":
                        the_game.nextGame()
                    if data["type"] == "old_game_request":
                        the_game.lastGame()

                    # RECEIVE: tile type filter
                    if data['type'] == 'toggle_tile_type':
                        print("message received", data)
                        await self.updateTileFilter(data)

                except asyncio.TimeoutError:
                    pass

                # delay
                await asyncio.sleep(.2)

            except websockets.ConnectionClosed:

                AdminServer.userlist.remove(websocket.remote_address)
                # print(f'''{TSTAMP()} {self.__class__.__name__} {
                #       websocket.remote_address} disconnected''')
                break

    async def updateTileFilter(self, message):
        '''Function to filter/ request data to server'''
        if message['type'] == 'toggle_tile_type':
            tile_type = message['tile_type']
            enabled = message['enabled']

            if enabled:
                self.enabled_tile_types.add(tile_type)
            else:
                self.enabled_tile_types.remove(tile_type)

    async def sendUnitData(self, websocket):
        '''
        Function to get and send unit data to web page
        '''

        unit_data_list = []

        for unit in Units.all_insts:

            # make data - tile:

            # make data - area: calc explored/ unexplored tiles
            explored = len(unit.travellog)
            maxtiles = unit.possibleTiles

            # make data - area: calc explored/ unexplored tiles
            data_tile = f"{explored} / {maxtiles}"
            data_rate = f"{(explored / maxtiles) * 100: 05.2f}%"

            # make NAME-DATA list
            unit_data = {
                "idunit": f"{unit.icon} #{unit.uniqueid}",
                # "object": f"{id(unit)}",
                "indx": f"{unit.this_tile.tile_index}",
                "move": f"{unit.move_numb}",
                "pass": f"{unit.moveRate}",
                "hits": f"{unit.move_hits}",
                "tile": f"{data_tile}",
                "rate": f"{data_rate}",
            }

            unit_data_list.append(unit_data)

        await websocket.send(json.dumps({
            "type": "unit_data_update",
            "data": unit_data_list
        }))

    async def sendUnitView(self, websocket):
        unit_view_data = []

        for unit in Units.all_insts:
            if unit.icon == EMOJI["KNIFE"]:

                unit_view_data.append({
                    "view": ViewData.makeUserView(unit)
                })

        await websocket.send(json.dumps({
            "type": "unit_view_update",
            "data": unit_view_data
        }))

    async def sendFullView(self, websocket):
        '''Function to send full grid view'''

        # make view
        fullview = ViewData.makeFullView()

        # send view
        await websocket.send(
            json.dumps({"type": "framebuffer", "data": fullview})
        )

    async def sendGameData(self, websocket):
        '''Function to get and send GameData to web page'''

        users_online = len(UserData.all_insts)

        game_data = {
            "Tile No.": len(Tiles.all_insts),
            "Unit No.": len(Units.all_insts),
            "Game Size": GameData.game_size,
            "View Size": GameData.view_size,
            "Stage No.": GameData.game_zone,
            "Prog. Uptime": GameData.gameTime(),
            "Stage Uptime": GameData.zoneTime(),
            "Admin Online": len(AdminServer.userlist),
            "Users Online": users_online,
        }

        await websocket.send(
            json.dumps({
                "type": "game_data",  # Choose a suitable type identifier
                "data": game_data
            })
        )

    async def sendLogData(self, websocket):
        '''Function to send game's log data to web page.'''

        # get log
        log_data = GameCore.log

        await websocket.send(json.dumps({
            "type": "log_data",
            "data": log_data
        }))

    async def sendNetData(self, websocket):
        '''Function to send client/server connection history data to web page.'''

        net_data = []

        for client in ClientServer.client_history:
            net_data.append({
                "ADDR": client.remote_address[0],
                "PORT": client.remote_address[1]
            })

        await websocket.send(json.dumps({
            "type": "net_data",
            "data": net_data
        }))

    async def sendUserData(self, websocket):
        '''Function to get and send user data/ view to web page'''
        user_data_list = []
        for user in UserData.all_insts:
            user_data_list.append({
                "User ID": user.user_numb,
                "Address": user.conn[0],
                "Time on": user.getTimeOnline,
                "Emoji": user.icon,
                "Index": user.this_tile.tile_index,
                "Moves": user.move_numb,
                "Lives": user.loss_numb,
                "view": ViewData.makeUserView(user),
            })

        await websocket.send(json.dumps({
            "type": "user_data_update",
            "data": user_data_list
        }))

    async def sendPrgmData(self, websocket):
        '''Function to send object and instance data to web page'''

        # Get the raw tile data
        tile_data = TileMeta.getEachInst(Tiles)

        # Format the data to match sendGameData structure
        data = {}
        for i, (key, value) in enumerate(tile_data.items()):
            data[key] = f"{value}"
            # print(key, value)

        await websocket.send(
            json.dumps({
                "type": "inst_data",
                "data": data
            })
        )

    async def sendServerData(self, websocket):
        '''Function to get and send server status information to the web page'''
        system_cpu, system_ram = monitor_server_load()

        # Get basic system information
        data = {
            "cpu": system_cpu,
            "ram": system_ram,
            "os": platform.system(),
            "node": platform.node(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "python": sys.version,
        }

        await websocket.send(
            json.dumps({
                "type": "server_data",
                "data": data
            })
        )

    async def sendTileData(self, websocket):
        '''
        Function to get and send tile data to the web page,
        filtering based on enabled tile types
        '''
        tile_data_list = []

        # Iterate over enabled tile types only
        for tile_type in self.tile_types:
            if tile_type.__name__ in self.enabled_tile_types:
                for tile in tile_type.all_insts:

                    tile_data_list.append({
                        "icon": f"{tile.tile_icon}",
                        "indx": f"{tile.tile_index}",
                        # "objc": f"{id(tile)}",
                        # "(xy)": f"({tile.tile_posx},{tile.tile_posy})",
                        "edge": f"{tile.tile_edge}",
                        "type": f"{tile.__class__.__name__}",
                        "uses": f"{len(tile.tile_uses)}",
                        "uniq": f"{tile.uniqUsed} / {len(Units.all_insts)}",
                        "last": f"{tile.tile_last_user} {tile.lastUsed}",
                    })

        await websocket.send(json.dumps({
            "type": "tile_data_update",
            "data": tile_data_list
        }))

    async def mainLoop(self):
        '''Main class function to start the server and send data.'''

        # SSL OFF
        self.server = await websockets.serve(
            self.handle_connection, self.ADDR, self.PORT
        )

        # SSL ON
        # self.server = await websockets.serve(
        #     self.handle_connection, self.ADDR, self.PORT, ssl=ssl_context)


class ClientServer(metaclass=SuperMeta):
    '''Server object for user connections'''
    clients = set()
    client_history = set()

    def __init__(self, ADDR, PORT):
        self.ADDR = ADDR
        self.PORT = PORT

        # report
        print(f"{TSTAMP()} USERS SERVER UP: {self.ADDR}:{self.PORT}")

    async def handle_connection(self, websocket, path):
        '''Handles individual client connections.'''

        # save conn. data, make user instance, spawn new user into game
        addr = websocket.remote_address
        new_user = UserData(websocket, addr)

        # pass the new conn. to the game as a new user
        UnitPool.spawnPlayer(new_user)
        ClientServer.clients.add(websocket)
        ClientServer.client_history.add(websocket)

        # start tasks: sending (game data) & receiving (input)
        await asyncio.gather(
            self.send_task(websocket, new_user),
            self.receive_task(websocket, new_user)
        )

        # remove user on disconnect
        print(TSTAMP(), "[cls.clnt]", new_user.conn,
              f"D/C:",  new_user.getTimeOnline)

        GameCore.clsLog(f'''{new_user.icon} {new_user.user_numb}: disconnect {
            new_user.getTimeOnline}''')

        ClientServer.clients.remove(websocket)
        UserData.all_insts.remove(new_user)

    async def send_task(self, websocket, user):
        '''Sends game state updates to the client.'''
        while True:
            try:

                # send game view
                game_board = ViewData.makeUserView(user)
                await websocket.send(json.dumps({"type": "gameState", "data": game_board}))

                # send users online
                users_online = len(UserData.all_insts)
                await websocket.send(
                    json.dumps({"type": "users_online", "data": users_online}))

                # send uptime
                uptime = GameData.gameTime()
                await websocket.send(
                    json.dumps({"type": "uptimeUpdate", "data": uptime})
                )

                await asyncio.sleep(0.05)
            except websockets.ConnectionClosed:
                break

    async def receive_task(self, websocket, user):
        '''Receives and processes user input.'''

        # Input rate limiting
        max_input_per_second = 6
        input_interval = 1.0 / max_input_per_second
        last_input_time = 0.0

        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)

                if data["type"] == "keypress":
                    current_time = time.monotonic()
                    if current_time - last_input_time >= input_interval:
                        user_input = data["data"]

                        print("REC", user_input)

                        GameCore.movePlayer(user, user_input)
                        last_input_time = current_time
                    else:
                        print(f'''{TSTAMP()} [cls.clnt] {
                              user.conn} input rate exceeded ({user_input})''')
            except websockets.ConnectionClosed:
                break

    async def mainLoop(self):
        # SSL OFF
        return await websockets.serve(self.handle_connection, self.ADDR, self.PORT)

        # SSL ON
        # return await websockets.serve(self.handle_connection, self.ADDR, self.PORT, ssl=ssl_context)


# EXECUTION
# ------------------------------------------------------------------------------


async def main():

    # network data
    ADDR = "0.0.0.0"
    PORT_CLNT = 5002
    PORT_ADMN = 5003

    # temp fix
    global the_game

    # make game manager - requires unit data
    the_game = GameCore()
    the_game_task = asyncio.create_task(the_game.gameLoop())

    # SSL for remote host
    # global ssl_context
    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # ssl_context.load_cert_chain("/etc/letsencrypt/live/bashgame.online/fullchain.pem",
    #                             "/etc/letsencrypt/live/bashgame.online/privkey.pem")

    # make network server - for admins
    the_admin_server = AdminServer(ADDR, PORT_ADMN)
    the_admin_server_task = asyncio.create_task(the_admin_server.mainLoop())

    # make network server - for clients
    the_client_server = ClientServer(ADDR, PORT_CLNT)
    the_client_server_task = asyncio.create_task(the_client_server.mainLoop())

    # start tasks
    await asyncio.gather(
        the_game_task,
        # the_control_task,
        the_admin_server_task,
        the_client_server_task,
    )


if __name__ == "__main__":
    # Run the main coroutine to start servers and event loop
    asyncio.run(main())
