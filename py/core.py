#!/usr/bin/python3


# game modules
from m_maps import *
from m_enemies import EntityData
from m_players import PlayerData
from m_tiles import *

# standard imports
import asyncio
import certifi
import copy
import json
# import math
import os
import psutil
import random
import ssl
import sys
import time
import websockets

from datetime import datetime

# HELP FUNC
# ------------------------------------------------------------------------------


def clear():
    """Function to clear terminal"""
    os.system("cls" if os.name == "nt" else "clear")


def monitor_server_load():
    process = psutil.Process()  # Get current process info
    cpu_percent = process.cpu_percent()
    memory_info = process.memory_info()
    rss_memory_mb = memory_info.rss / (1024 ** 2)  # Calculate in MB
    rss_memory_mb = int(rss_memory_mb)  # Convert to integer

    # print(f"CPU Usage: {cpu_percent}%")
    # print(f"Memory Usage (RSS): {rss_memory_mb} MB")

    return cpu_percent, rss_memory_mb


def TSTAMP():
    now = datetime.now()
    now = now.strftime("%y%m%d %H:%M:%S.%f")
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

        while aggressor.points_hp > 0:
            # defender gets first strike; i.e., never the player
            aggressor.takeDamage(defender.points_at)
            defender.takeDamage(aggressor.points.at)

            if aggressor.isLiving:
                return True
            else:
                return False


class GameData:
    """Class to hold data for level design."""

    BOARDS = {
        # needs zero place for first loop
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

    def __init__(self) -> None:
        """Function to initialize game data for each level or stage."""

        # gamesize: must be perfect square.
        # VIEWSIZE: must be odd and <= (2 * VIEWSIZE - 1)

        self.stage = 0
        self.stage_time = datetime.now()

        self.VIEWSIZE = 9
        self.EDGESIZE = self.VIEWSIZE // 2 + 1
        self.gamesize = self.BOARDS[self.stage]

    def nextStage(self):
        print(TSTAMP(), "Next Stage")
        self.stage += 1
        self.gamesize = self.BOARDS[self.stage]


class SpawnPool:
    """Class to hold spawn templates."""

    def __init__(self, gamedata_inst) -> None:

        # load game data
        self.GameData = gamedata_inst

    def autoPopulate(self):
        """Function to make entities based on map size"""

        # wipe all
        EntityData.all_insts = []

        # get map data
        self.gamesize = self.GameData.gamesize
        self.EDGESIZE = self.GameData.EDGESIZE

        # make wolves
        EntityData.factory(
            quantity=self.gamesize // 2,
            UNIT_ICON=EntityData.EMOJI["WOLF"],
            MOVE_TYPE="idle",
            HOME_TILE=EMOJI['WOODS'],
        )

        # make knives
        EntityData.factory(
            quantity=self.gamesize // 36,
            UNIT_ICON=EntityData.EMOJI["KNIFE"],
            MOVE_TYPE="hunt",
            HOME_TILE=EMOJI['WOODS'],
        )

        # make spiders
        EntityData.factory(
            quantity=self.gamesize // 10,
            UNIT_ICON=EntityData.EMOJI["SPIDER"],
            MOVE_TYPE="idle",
            HOME_TILE=EMOJI['CABIN'],
        )


class GameMaster:
    """Class to manage all game logic elements."""

    log = []

    # level/ stage number, time on level, server uptime
    game_numb = 0
    game_time = 0
    uptime = 0

    def __init__(self, gamedata_inst, spawner_inst) -> None:

        # save server start time
        GameMaster.uptime = datetime.now()

        # link core game objects for access
        self.GameData = gamedata_inst
        self.SpawnPool = spawner_inst

        # make new game
        self.newGame()

    def randomIndex(self):
        """Function to pick random WOODS index."""
        while True:
            random_index = random.randint(
                0, self.GameData.gamesize * self.GameData.gamesize - 1)
            if self.framebuffer[random_index] == EMOJI['WOODS']:
                return random_index

    def randomIndexType(self, entity):
        """Function to pick random valid index."""
        while True:
            random_index = random.randint(
                0, self.GameData.gamesize * self.GameData.gamesize - 1)
            if self.framebuffer[random_index] == entity.HOME_TILE:
                return random_index

    def getIndexfromXY(self, x, y):
        """Function to convert from X,Y to POSITION"""
        index = y * self.GameData.gamesize + x
        return index

    def getXYFromIndex(self, index):
        """Function to convert from POSITION to X,Y"""
        x = index % self.GameData.gamesize
        y = index // self.GameData.gamesize
        return x, y

    # SERVER STATES

    @classmethod
    def getUptime(cls):
        """Calculates and returns the server uptime as a formatted string."""
        uptime = datetime.now() - cls.uptime
        uptime = str(uptime)
        uptime = uptime[:-4]
        return uptime

    @classmethod
    def clsLog(cls, string: str):
        """Class function to timestamp and save notifications."""

        string = f"""{TSTAMP()} [cls.Game] {string}"""
        cls.log.append(string)

    @classmethod
    def shutdown(cls):
        """Function to force quit."""
        sys.exit(0)

    def getTileType(self, index):
        """Get tile type at index"""
        tiletype = self.emojimap[index]
        return tiletype

    # DISPLAY & SCREEN AREA

    def updateFramebuffer(self):
        """Function to manage static map & dynamic overlay"""

        # brute-force regen of framebuffer
        # self.framebuffer = copy.deepcopy(self.TileLand.tilemap)
        self.framebuffer = copy.deepcopy(TileLand.tilemap)

        # add players to framebuffer
        for player in PlayerData.all_insts:

            # add headstones to framebuffer
            for index in player.loss_area:
                self.framebuffer[index] = EMOJI["HEADSTONE"]

            # add player after headstone (z-position logic)
            self.framebuffer[player.position] = player.icon

        # add enemies to framebuffer
        for entity in EntityData.all_insts:
            self.framebuffer[entity.position] = entity.UNIT_ICON

    def getPlayerView(self, player):
        """Function to draw a small range of the map centered on an index.
        Returns a square array of [player.viewradius] size for a given player.
        Uses grid logic; for each row, for each col, check tile."""

        # update the framebuffer before calculating render window
        self.updateFramebuffer()

        # calc view dist
        lower_bound = player.viewradi * -1
        offsets = []
        output = []

        # make range
        for i in range(player.viewsize):
            offsets.append(lower_bound)
            lower_bound += 1

        for yoff in offsets:
            for xoff in offsets:
                new_offset = xoff + \
                    (yoff * self.GameData.gamesize) + player.position

                # or draw it normally - not cabin view
                tile_to_draw = self.framebuffer[new_offset]

                # save to list for transmission to client
                output.append(tile_to_draw)

        # return the array of display data
        return output

    # GAME OPERATIONS

    def spawnPlayer(self, player):
        """Function to put player at starting index"""
        player.lastposi = None
        player.position = (self.GameData.gamesize *
                           self.GameData.gamesize) // 2 + (self.GameData.gamesize // 2)

        GameMaster.clsLog(f"""{player.icon} {player.user_numb}: spawns.""")

    def initEntities(self):
        for entity in EntityData.all_insts:
            entity.position = self.randomIndexType(entity)
            entity.lastposi = copy.deepcopy(entity.position)

    def respawnEntity(self, entity):
        """Function to place entity at random valid index"""

        # spawn entity to HOME_TILE type
        entity.position = self.randomIndexType(entity)
        entity.lastposi = copy.deepcopy(entity.position)

    def moveAllEntities(self):
        """Function to move every entity"""

        # move each entity by its move type
        for entity in EntityData.all_insts:
            if entity.MOVE_TYPE == "idle":
                self.moveEntityIdle(entity)
            if entity.MOVE_TYPE == "hunt":
                self.moveEntityHunt(entity)

    def moveEntityIdle(self, entity):
        """Primary movement method; one tile NSEW"""

        # save call; save last tile
        entity.move_numb += 1
        entity.lastposi = entity.position

        # choose random direction
        next_move = random.randint(0, 3)

        if next_move == 0:
            entity.position += 1
        if next_move == 1:
            entity.position -= 1
        if next_move == 2:
            entity.position += self.GameData.gamesize
        if next_move == 3:
            entity.position -= self.GameData.gamesize

        # if new tile is not compatible type, revert movement
        if self.TileLand.tilemap[entity.position] != entity.HOME_TILE:
            entity.position = entity.lastposi
            entity.move_fail += 1
            return 1

        entity.move_succ += 1

    def movePlayer(self, player, player_input):
        """Function to process player hardware input to action"""

        # save last
        player.lastposi = copy.deepcopy(player.position)

        # placeholder
        new_offset = 0

        if player_input == "w":
            new_offset = -self.GameData.gamesize
        elif player_input == "s":
            new_offset = self.GameData.gamesize
        elif player_input == "a":
            new_offset = -1
        elif player_input == "d":
            new_offset = 1

        # print("PLAYER INDEX @ ", player.position + new_offset)

        # readability: get player's occupied tile type & next tile type
        last_tile = Tiles.all_insts[player.position]
        next_tile = Tiles.all_insts[player.position + new_offset]

        # is tile passable
        if not next_tile.tile_pass:
            return 1

        # block cabins - entry
        if next_tile.tile_name == "cabin":
            if not last_tile.tile_name in next_tile.tile_link:
                return 1

        # block cabins - exit
        if last_tile.tile_name == "cabin":
            if next_tile.tile_name not in last_tile.tile_link:
                return 1

        # block players by index
        for some_player in PlayerData.all_insts:
            if player.position + new_offset == some_player.position:
                return 1

        # finalize move
        player.lastposi = copy.deepcopy(player.position)
        player.move_numb += 1
        player.position += new_offset

        GameMaster.clsLog(f"""{player.icon} {player.user_numb}: move #{
                          player.move_numb}""")
        return 0

    def moveEntityHunt(self, entity):
        """
        Function to move ARG1 [entity] @ target index.
        Entities hunting effectively take two turns thus moving diagonally.
        """

        # find nearest target
        target_index = PlayerData.getNearestPlayer(entity.position)

        if target_index == None:
            # results in entity moving to returned index
            return 1

        # save last/current tile
        entity.lastposi = entity.position

        # move at target
        entity.move_numb += 1

        # convert indices to x,y for comparison
        entity_x, entity_y = self.getXYFromIndex(entity.position)
        target_x, target_y = self.getXYFromIndex(target_index)

        # entity horizontal movement
        if entity_x < target_x:
            entity_x += 1
        if entity_x > target_x:
            entity_x -= 1

        # make new index from x,y
        new_index = self.getIndexfromXY(entity_x, entity_y)

        # check tile - approve
        if self.emojimap[new_index] not in TileLand.ENEMIES_INVALID_TILES:
            entity.position = new_index
            entity.move_succ += 1

        # convert indices to x,y for comparison
        entity_x, entity_y = self.getXYFromIndex(entity.position)

        # entity vertical movement
        if entity_y < target_y:
            entity_y += 1
        if entity_y > target_y:
            entity_y -= 1

        # make new index
        new_index = self.getIndexfromXY(entity_x, entity_y)

        # check tile - approve
        if self.emojimap[new_index] not in TileLand.ENEMIES_INVALID_TILES:
            entity.position = new_index
            entity.move_succ += 1

        # teleport if stuck after X turns // 2
        if entity.position == entity.lastposi:
            entity.move_skip += 1
            if entity.move_skip == 6:
                entity.move_skip = 0
                entity.position = self.randomIndex()

    # GAME STATES

    def gameOver(self):
        """Function to check for player loss or level complete."""
        pass

        for player in PlayerData.all_insts:

            # save player tile type
            # player_tile_type = self.getTileType(player.position)
            player_tile = Tiles.all_insts[player.position]
            player_tile_type = player_tile.tile_icon

            # did player hit loss tile
            if player_tile.tile_trap:
                print(player.icon, player_tile.tile_trap_text)

                GameMaster.clsLog(
                    f"""{player.icon} {player.user_numb}
                        {player_tile.tile_trap_text}"""
                )

                player.recordLoss()
                self.spawnPlayer(player)

            # did player hit exit
            if player_tile_type == EMOJI["SAVED"]:
                self.newGame()

                GameMaster.clsLog(f"""{player.icon} wins!""")

            # did player hit enemy
            for entity in EntityData.all_insts:
                if player.position == entity.position:

                    # FIGHT

                    # if not ArenaData.battMode(player, entity):

                    player.recordLoss()
                    self.respawnEntity(entity)
                    self.spawnPlayer(player)

                    # log
                    print(TSTAMP(), "[cls.game]", player.conn,
                          "hits", entity.UNIT_ICON, "#", player.loss_numb)
                    GameMaster.clsLog(
                        f"""{entity.UNIT_ICON} > {player.icon} {player.user_numb}: #{player.loss_numb}""")

    def newGame(self):
        """Function to make new game while network is active."""

        # reset game log
        # GameMaster.log = []
        GameMaster.game_time = datetime.now()
        GameMaster.game_numb += 1
        GameMaster.clsLog(f"""NEW GAME #{self.game_numb}""")

        # increment stage
        self.GameData.nextStage()

        # destroy tiles
        Tiles.all_calls = 0
        Tiles.all_insts = []
        self.TileLand = TileLand(
            self.GameData.gamesize, self.GameData.EDGESIZE)

        # link map & make framebuffer (editable map)
        self.emojimap = tuple(self.TileLand.tilemap)
        self.framebuffer = list(self.emojimap)

        # make players
        for player in PlayerData.all_insts:
            self.spawnPlayer(player)

        # make enemies
        self.SpawnPool.autoPopulate()
        self.initEntities()

    async def gameLoop(self):
        """Coroutine to execute main game loop logic"""

        last_move_times = {}

        while True:

            # MOVE ENTITIES

            current_time = time.time()
            for entity in EntityData.all_insts:
                if entity not in last_move_times:
                    # Initialize last move time
                    last_move_times[entity] = current_time

                time_since_last_move = current_time - last_move_times[entity]
                if time_since_last_move >= entity.move_rate:
                    if entity.MOVE_TYPE == "idle":
                        self.moveEntityIdle(entity)
                    if entity.MOVE_TYPE == "hunt":
                        self.moveEntityHunt(entity)
                    # Update last move time
                    last_move_times[entity] = current_time

            # is game over
            self.gameOver()

            # update display, for now
            self.updateFramebuffer()

            # game loop speed
            await asyncio.sleep(.025)


class ComMan:
    """Class for a terminal interface."""

    def __init__(self, game_master_inst):
        self.game = game_master_inst
        pass

    async def commLoop(self):  # Asynchronous main loop
        """Server control interface mainloop using asynchronous input."""
        while True:
            clear()
            print("Menu")
            print("  1 - Show All Players ")
            print("  2 - Dump Tile Map")
            print("  3 - Resource Monitor")
            print("  4 - View Game log")
            print("  5 - New Game")
            print("  9 - End Program")
            print()

            choice = await self.getUserChoice()

            if choice == 1:
                PlayerData.listAllPlayers()
                # Await the blocking 'input' call
                await asyncio.to_thread(input, "Press ENTER")

            elif choice == 2:

                date_str = datetime.now().strftime("%y%m%d-%H:%M:%S.%f")
                filename = f"{date_str}_tilemap.txt"

                # Open the file for writing in text mode
                with open(filename, 'w') as file:
                    # Need array dimension to write lines
                    size = len(TileLand.tilemap)
                    size = math.sqrt(size)
                    size = int(size)

                    # Write each tile to the file
                    for line in range(size):
                        for item in TileLand.tilemap[line * size:(line + 1) * size]:
                            file.write(item)
                        # Add a newline character at the end of each line
                        file.write('\n')

            elif choice == 3:
                clear()
                monitor_server_load()
                await asyncio.sleep(1)

            elif choice == 4:
                clear()
                for line in GameMaster.log:
                    print(line)
                input()

            elif choice == 5:
                clear()
                self.game.newGame()

            elif choice == 9:
                clear()
                raise KeyboardInterrupt  # Exit the loop using an exception

    async def getUserChoice(self):
        """Asynchronously waits for valid user input."""
        while True:
            try:
                # Use asyncio.to_thread for non-blocking inpute
                choice = int(await asyncio.to_thread(input, "Press [#]"))
                print()
                if 1 <= choice <= 9:
                    return choice
                else:
                    print("Please enter a number between 1 and 9.")
            except ValueError:
                print("Please enter a number.")
            await asyncio.sleep(0.25)


class AdminServer:
    """Server object to send data to HTML interface."""

    def __init__(self, ADDR, PORT, GameData) -> None:
        self.network_addr = ADDR
        self.admin_port = PORT
        self.server = None

        # import game data
        self.GameData = GameData

    async def handle_connection(self, websocket, path):
        """Handles incoming connections from admin clients and sends updates."""

        # notify connection
        print(f"""{TSTAMP()} [cls.admn] {
            websocket.remote_address} connected""")

        while True:
            try:
                # datas to send
                await self.sendEntityData(websocket)
                await self.sendEntityView(websocket)
                await self.sendFramebuffer(websocket)
                await self.sendGameData(websocket)
                await self.sendLogData(websocket)
                await self.sendNetData(websocket)
                await self.sendPlayerData(websocket)
                await self.sendServerStatus(websocket)

                try:
                    # datas to receive
                    # set timeout as needed
                    message = await asyncio.wait_for(websocket.recv(), timeout=0.1)

                    data = json.loads(message)
                    if data["type"] == "new_game_request":
                        the_game.newGame()

                except asyncio.TimeoutError:
                    pass

                # delay
                await asyncio.sleep(.1)

            except websockets.ConnectionClosed:

                print(f"""{TSTAMP()} [cls.admn] {
                      websocket.remote_address} disconnected""")
                break

    async def sendFramebuffer(self, websocket):
        framebuffer = the_game.framebuffer
        await websocket.send(
            json.dumps({"type": "framebuffer", "data": framebuffer})
        )

    async def sendEntityData(self, websocket):
        """
        Function to get and send entity data to web page
        """
        entity_data_list = []

        for entity in EntityData.all_insts:
            entity_data = {
                "serial": f"{entity.uniqueid:04d}",
                "icon": f"{entity.UNIT_ICON}",
                "indx": f"{entity.position:06d}",
                "move": f"{entity.move_numb:06d}",
                "rate": f"{entity.moveRate}",
            }

            # Include the view data ONLY for knives
            if entity.UNIT_ICON == EntityData.EMOJI["KNIFE"]:
                entity_data["view"] = the_game.getPlayerView(entity)

            entity_data_list.append(entity_data)

        await websocket.send(json.dumps({
            "type": "entity_data_update",
            "data": entity_data_list
        }))

    async def sendEntityView(self, websocket):
        entity_view_data = []

        for entity in EntityData.all_insts:
            if entity.UNIT_ICON == EntityData.EMOJI["KNIFE"]:
                entity_view_data.append({
                    "view": the_game.getPlayerView(entity)
                })

        await websocket.send(json.dumps({
            "type": "entity_view_update",
            "data": entity_view_data
        }))

    async def sendGameData(self, websocket):
        """Function to get and send GameData to web page"""
        game_data = {
            "Game Size": self.GameData.gamesize,
            "View Size": self.GameData.VIEWSIZE,
            "Stage No.": self.GameData.stage,
            # "Game Time": self.GameData.stage_time,
        }

        await websocket.send(
            json.dumps({
                "type": "game_data",  # Choose a suitable type identifier
                "data": game_data
            })
        )

    async def sendLogData(self, websocket):
        """Function to send game's log data to web page."""

        # get log
        log_data = GameMaster.log

        await websocket.send(json.dumps({
            "type": "log_data",
            "data": log_data
        }))

    async def sendNetData(self, websocket):
        """Function to send client/server connection history data to web page."""

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

    async def sendPlayerData(self, websocket):
        """Function to get and send player data/ view to web page"""
        player_data_list = []
        for player in PlayerData.all_insts:
            player_data_list.append({
                "User ID": player.user_numb,
                "Address": player.conn[0],
                "Time on": player.getTimeOnline,
                "Emoji": player.icon,
                "Index": player.position,
                "Moves": player.move_numb,
                "Lives": player.loss_numb,
                "view": the_game.getPlayerView(player),
            })

        await websocket.send(json.dumps({
            "type": "player_data_update",
            "data": player_data_list
        }))

    async def sendServerStatus(self, websocket):
        """Function to get and send both server-uptime and users-online to web page"""
        system_cpu, system_ram = monitor_server_load()
        uptime = GameMaster.getUptime()
        users_online = len(PlayerData.all_insts)
        await websocket.send(
            json.dumps({
                "type": "server_data",
                "data": {
                    "cpu": system_cpu,
                    "ram": system_ram,
                    "uptime": uptime,
                    "online": users_online,
                }
            })
        )

    async def mainLoop(self):
        """Main class function to start the server and send data."""

        # SSL OFF
        self.server = await websockets.serve(
            self.handle_connection, self.network_addr, self.admin_port
        )

        # SSL ON
        # self.server = await websockets.serve(
        #     self.handle_connection, self.network_addr, self.admin_port, ssl=ssl_context)


class ClientServer:

    clients = set()
    client_history = set()

    def __init__(self, ADDR, PORT, game):
        self.ADDR = ADDR
        self.PORT = PORT

        # game instance needed to send game data to player
        self.game = game

    async def handle_connection(self, websocket, path):
        """Handles individual client connections."""

        # save conn. data, make player instance, spawn new player into game
        addr = websocket.remote_address
        new_player = PlayerData(websocket, addr)

        # pass the new conn. to the game as a new player
        self.game.spawnPlayer(new_player)

        ClientServer.clients.add(websocket)
        ClientServer.client_history.add(websocket)

        # start tasks: sending (game data) & receiving (input)
        await asyncio.gather(
            self.send_task(websocket, new_player),
            self.receive_task(websocket, new_player)
        )

        # remove player on disconnect
        print(TSTAMP(), "[cls.clnt]", new_player.conn, "disconnected")
        GameMaster.clsLog(f"""{new_player.icon} {new_player.user_numb}: disconnected after {
                          new_player.getTimeOnline()}""")

        ClientServer.clients.remove(websocket)
        PlayerData.all_insts.remove(new_player)

    async def send_task(self, websocket, player):
        """Sends game state updates to the client."""
        while True:
            try:

                # send game view
                game_board = self.game.getPlayerView(player)
                await websocket.send(json.dumps({"type": "gameState", "data": game_board}))

                # send users online
                users_online = len(PlayerData.all_insts)
                await websocket.send(
                    json.dumps({"type": "users_online", "data": users_online}))

                # send uptime
                uptime = GameMaster.getUptime()
                await websocket.send(
                    json.dumps({"type": "uptimeUpdate", "data": uptime})
                )

                await asyncio.sleep(0.05)
            except websockets.ConnectionClosed:
                break

    async def receive_task(self, websocket, player):
        """Receives and processes player input."""

        # Input rate limiting
        max_input_per_second = 6
        input_interval = 1.0 / max_input_per_second
        last_input_time = 0.0

        while True:
            try:
                message = await websocket.recv()
                data = json.loads(message)

                if data["type"] == "playerInput":
                    current_time = time.monotonic()
                    if current_time - last_input_time >= input_interval:
                        player_input = data["data"]
                        self.game.movePlayer(player, player_input)
                        last_input_time = current_time
                    else:
                        print(f"""{TSTAMP()} [cls.clnt] {
                              player.conn} input rate exceeded ({player_input})""")
            except websockets.ConnectionClosed:
                break

    async def mainLoop(self):
        # SSL OFF
        return await websockets.serve(self.handle_connection, self.ADDR, self.PORT)

        # SSL ON
        # return await websockets.serve(self.handle_connection, self.ADDR, self.PORT, ssl=ssl_context)


# EXECUTION
# -------------------------------------------------------------------------------


async def main():

    # network data
    ADDR = "0.0.0.0"
    PORT_CLNT = 5002
    PORT_ADMN = 5003

    # temp fix
    global the_game

    # make data
    the_data = GameData()

    # make game board - requires game data
    # the_site = MapData(the_data.gamesize, the_data.EDGESIZE)

    # make unit manager - requires game data
    the_guys = SpawnPool(the_data)

    # make game manager - requires unit data
    the_game = GameMaster(the_data, the_guys)
    the_game_task = asyncio.create_task(the_game.gameLoop())

    # make terminal interface
    the_control = ComMan(the_game)
    the_control_task = asyncio.create_task(the_control.commLoop())

    # SSL for remote host
    # global ssl_context
    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # ssl_context.load_cert_chain("/etc/letsencrypt/live/bashgame.online/fullchain.pem",
    #                             "/etc/letsencrypt/live/bashgame.online/privkey.pem")

    # make network server - for admins
    the_admin_server = AdminServer(ADDR, PORT_ADMN, the_data)
    the_admin_server_task = asyncio.create_task(the_admin_server.mainLoop())

    # make network server - for clients
    the_client_server = ClientServer(ADDR, PORT_CLNT, the_game)
    the_client_server_task = asyncio.create_task(the_client_server.mainLoop())

    # start tasks
    await asyncio.gather(
        the_game_task,
        the_control_task,
        the_admin_server_task,
        the_client_server_task,
    )


if __name__ == "__main__":
    # Run the main coroutine to start servers and event loop
    asyncio.run(main())
