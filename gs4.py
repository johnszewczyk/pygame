#!/usr/bin/python3

# non-standard imports
import kbhit

# game modules
from m_maps import MapData
from m_enemies import EntityData
from m_players import PlayerData

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


################################################################################


class LogMe:
    """LogMe class: shorthand for logging text."""

    lm_i = []
    lm_n = []
    lm_s = []

    def __init__(self) -> None:
        pass

    @classmethod
    def linp(cls, string):
        cls.lm_i.append(LogMe.tStamp() + " " + string)

    @classmethod
    def lnet(cls, string):
        cls.lm_n.append(LogMe.tStamp() + " " + string)

    @classmethod
    def lsen(cls, string):
        cls.lm_s.append(LogMe.tStamp() + " " + string)

    @staticmethod
    def tStamp():
        now = datetime.now()
        now = now.strftime("%y-%m-%d-%H:%M:%S.%f")
        return now

    @classmethod
    def seeLog(cls, log):
        for line in log:
            print(line)

    @classmethod
    def saveText(cls):
        """Function to write logs to disk"""
        log_files = [
            ("log-input.txt", cls.lm_i),
            ("log-network.txt", cls.lm_n),
            ("log-sent.txt", cls.lm_s),
        ]

        for filename, log_data in log_files:
            with open(
                filename, "a"
            ) as f:  # Use "a" (append) mode to create if not exists
                for log in log_data:
                    f.write(log + "\n")


class GameMaster:
    """Class to manage all game logic elements."""

    log = []

    # GAMESIZE: must be perfect square.
    # VIEWSIZE: must be odd and <= (2 * VIEWSIZE - 1)
    GAMESIZE = 169
    EDGESIZE = 5
    VIEWSIZE = 9
    VIEWRADI = (VIEWSIZE - 1) // 2

    # level/ stage number, time on level, server uptime
    game_numb = 0
    game_time = 0
    uptime = 0

    def __init__(self) -> None:

        # save server start time
        GameMaster.uptime = datetime.now()

        # make new game
        self.newGame()

    def createEntities(self):
        """Function to make entities based on map size"""

        # make wolves
        quantity = self.GAMESIZE // 2
        for x in range(quantity):
            new_entity = EntityData(
                icon=EntityData.EMOJI["WOLF"],
                movetype="idle",
                index=self.randomIndex(),
                hometile=MapData.EMOJI['WOODS'],
            )

        # make knives
        quantity = 1
        for x in range(quantity):
            new_entity = EntityData(
                icon=EntityData.EMOJI["KNIFE"],
                movetype="hunt",
                index=self.randomIndex()
                hometile=MapData.EMOJI['WOODS'],

            )

        # make spiders

    def randomIndex(self):
        """Function to pick random valid index."""
        while True:
            random_index = random.randint(
                0, GameMaster.GAMESIZE * GameMaster.GAMESIZE - 1)
            if self.MapData.tilemap[random_index] == MapData.EMOJI['WOODS']:
                return random_index

    def getIndexfromXY(self, x, y):
        """Function to convert from X,Y to POSITION"""
        index = y * GameMaster.GAMESIZE + x
        return index

    def getXYFromIndex(self, index):
        """Function to convert from POSITION to X,Y"""
        x = index % GameMaster.GAMESIZE
        y = index // GameMaster.GAMESIZE
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
    def loggit(cls, string):
        """Class function to timestamp and save notifications."""
        now = datetime.now()
        now = now.strftime("%y%m%d-%H:%M:%S.%f")
        now = now[:18]

        string = str(now + " " + string)
        cls.log.append(string)

    @classmethod
    def shutdown(cls):
        """Function to force quit."""
        sys.exit(0)

    def getTileType(self, index):
        """Get tile type at index"""
        tiletype = self.gamemap[index]
        return tiletype

    # DISPLAY & SCREEN AREA

    def updateFramebuffer(self):
        """Function to manage dynamic visual elements"""

        # brute-force regen of framebuffer
        self.framebuffer = copy.deepcopy(self.MapData.tilemap)

        # add players to framebuffer
        for player in PlayerData.all_instances:

            # add each headstones to framebuffer
            for index in player.loss_area:
                self.framebuffer[index] = MapData.EMOJI["HEADSTONE"]

            # add player after headstone (z-position logic)
            self.framebuffer[player.position] = player.icon

        # add enemies to framebuffer
        for entity in EntityData.all_instances:
            self.framebuffer[entity.position] = entity.icon

    def showFramebuffer(self):
        """Print the framebuffer array until user input."""

        # Non-blocking input handling
        kb = kbhit.KBHit()
        userchar = "0"

        while True:
            clear()

            line = 0
            for tile in self.framebuffer:
                line += 1
                print(tile, end="")

                if line == GameMaster.GAMESIZE:
                    line = 0
                    print()

            print("PRESS ESC TO BREAK")
            if kb.kbhit():
                userchar = kb.getch()

            fps = 6
            time.sleep(1 / fps)

            if ord(userchar) == 27:  # Break on ESC key
                break

    def getPlayerView1(self, player):
        """Function to draw a small range of the map centered on an index.
        Returns a square array of [player.viewradius] size for a given player.
        Uses grid logic; for each row, for each col, check tile."""

        # update the framebuffer before calculating render window
        self.updateFramebuffer()

        # calc view dist
        lower_bound = GameMaster.VIEWRADI * -1
        offsets = []
        output = []

        # make range
        for i in range(GameMaster.VIEWSIZE):
            offsets.append(lower_bound)
            lower_bound += 1

        for yoff in offsets:
            for xoff in offsets:
                new_offset = xoff + \
                    (yoff * GameMaster.GAMESIZE) + player.position

                # CABIN VIEW

                # if the player is standing on a cabin tile...
                if self.MapData.tilemap[player.position] == MapData.EMOJI["CABIN"]:

                    # if the tile-to-draw is not visible from cabin tile, OR if it is a floor tile...
                    if self.framebuffer[new_offset] not in (
                        [
                            MapData.EMOJI["CABIN"],
                            MapData.EMOJI["DOOR"],
                            MapData.EMOJI["HUMAN"],
                            MapData.EMOJI["WRECKED"],
                        ]
                        + PlayerData.EMOJI

                    ):

                        # replace with empty tile
                        tile_to_draw = MapData.EMOJI["EMPTY"]
                    else:

                        # or draw it normally - it's visible during cabin view
                        tile_to_draw = self.framebuffer[new_offset]

                else:
                    # or draw it normally - not cabin view
                    tile_to_draw = self.framebuffer[new_offset]

                # save to list for transmission to client
                output.append(tile_to_draw)

        # return the array of display data
        return output

    def getPlayerView(self, player):
        """Function to draw a small range of the map centered on an index.
        Returns a square array of [player.viewradius] size for a given player.
        Uses grid logic; for each row, for each col, check tile."""

        # update the framebuffer before calculating render window
        self.updateFramebuffer()

        # calc view dist
        lower_bound = GameMaster.VIEWRADI * -1
        offsets = []
        output = []

        # make range
        for i in range(GameMaster.VIEWSIZE):
            offsets.append(lower_bound)
            lower_bound += 1

        for yoff in offsets:
            for xoff in offsets:
                new_offset = xoff + \
                    (yoff * GameMaster.GAMESIZE) + player.position

                # CABIN VIEW

                # if the player is standing on a cabin tile...
                if self.MapData.tilemap[player.position] == MapData.EMOJI["CABIN"]:

                    # if the tile-to-draw is not visible from cabin tile, OR if it is a floor tile...
                    if self.framebuffer[new_offset] not in (
                        [
                            MapData.EMOJI["CABIN"],
                            MapData.EMOJI["DOOR"],
                            MapData.EMOJI["GRAVE"],
                            MapData.EMOJI["HUMAN"],
                            MapData.EMOJI["WRECKED"],
                        ]
                        + PlayerData.EMOJI

                    ):

                        # replace with empty tile
                        tile_to_draw = MapData.EMOJI["EMPTY"]

                    if self.MapData.isFloorTile(new_offset) and new_offset != player.position:

                        # replace with empty tile
                        tile_to_draw = MapData.EMOJI["EMPTY"]

                    else:

                        # or draw it normally - it's visible during cabin view
                        tile_to_draw = self.framebuffer[new_offset]

                else:
                    # or draw it normally - not cabin view
                    tile_to_draw = self.framebuffer[new_offset]

                # save to list for transmission to client
                output.append(tile_to_draw)

        # return the array of display data
        return output

    # GAME OPERATIONS

    def spawnPlayer(self, player):
        """Function to put player at starting index"""
        player.last_pos = None
        player.position = self.MapData.GRID_SW

        GameMaster.loggit(f"""{player.icon} spawns.""")

    def spawnEntity(self, entity):
        """Function to place entity at random index"""
        entity.position = self.randomIndex()
        entity.last_pos = copy.deepcopy(entity.position)

    def spawnInitial(self):
        for entity in EntityData.all_instances:
            self.spawnEntity(entity)

    def moveAllEntities(self):
        """Function to move every entity"""

        # move each entity by its move type
        for entity in EntityData.all_instances:
            if entity.movetype == "idle":
                self.moveEntityIdle(entity)
            if entity.movetype == "hunt":
                self.huntHuman(entity)

    def moveEntityIdle(self, entity):
        """Primary movement method; one tile NSEW"""

        # save last/current tile
        entity.last_pos = entity.position

        # choose random direction
        next_move = random.randint(0, 3)

        if next_move == 0:
            entity.position += 1
        if next_move == 1:
            entity.position -= 1
        if next_move == 2:
            entity.position += GameMaster.GAMESIZE
        if next_move == 3:
            entity.position -= GameMaster.GAMESIZE

        # if new tile is not compatible type, revert movement
        if self.MapData.tilemap[entity.position] != MapData.EMOJI["WOODS"]:
            entity.position = entity.last_pos
            return 1

        entity.move_numb += 1

    def movePlayer(self, player, player_input):
        """Function to process player hardware input to action"""

        # save last
        player.last_pos = copy.deepcopy(player.position)

        # placeholder
        new_offset = 0

        if player_input == "w":
            new_offset = -GameMaster.GAMESIZE
        elif player_input == "s":
            new_offset = GameMaster.GAMESIZE
        elif player_input == "a":
            new_offset = -1
        elif player_input == "d":
            new_offset = 1

        # readability: get player's occupied tile type & next tile type
        last_type = self.getTileType(player.position)
        next_type = self.gamemap[player.position + new_offset]

        # validate move

        # block tiles absolutely
        if next_type in MapData.PLAYERS_INVALID_TILES:
            return 1

        # block players, by index
        for some_player in PlayerData.all_instances:
            if player.position + new_offset == some_player.position:
                return 1

        # block cabins if not on cabin or door
        if next_type == MapData.EMOJI["CABIN"]:
            if last_type not in (MapData.EMOJI["CABIN"], MapData.EMOJI["DOOR"]):
                return 1

        # block woods from cabin
        if next_type == MapData.EMOJI["WOODS"]:
            if last_type == MapData.EMOJI["CABIN"]:
                return 1

        # block water from cabin
        if next_type == MapData.EMOJI["WATER"]:
            if last_type == MapData.EMOJI["CABIN"]:
                return 1

        # block weeds from cabin
        if next_type == MapData.EMOJI["FIELD"]:
            if last_type == MapData.EMOJI["CABIN"]:
                return 1

        # finalize move
        player.last_pos = copy.deepcopy(player.position)
        player.move_numb += 1
        player.position += new_offset

        GameMaster.loggit(f"""{player.icon} move #{player.move_numb}""")
        return 0

    def huntHuman(self, entity):
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
        entity.last_pos = entity.position

        # move at target

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
        if self.gamemap[new_index] not in MapData.ENEMIES_INVALID_TILES:
            entity.position = new_index
            entity.move_numb += 1

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
        if self.gamemap[new_index] not in MapData.ENEMIES_INVALID_TILES:
            entity.position = new_index
            entity.move_numb += 1

        # teleport if stuck
        if entity.position == entity.last_pos:
            entity.same_tile += 1
            if entity.same_tile == 6:
                entity.same_tile = 0
                entity.position = self.randomIndex()

    # GAME STATES

    def gameOver(self):
        """Function to check for player loss or level complete."""

        for player in PlayerData.all_instances:

            # save player tile type
            player_tile_type = self.getTileType(player.position)

            # did player hit loss tile
            if player_tile_type in [
                MapData.EMOJI["WATER"],
                MapData.EMOJI["WRECKED"],
            ]:
                if player_tile_type == MapData.EMOJI["WATER"]:
                    GameMaster.loggit(f"""{player.icon} drowned.""")
                if player_tile_type == MapData.EMOJI["WRECKED"]:
                    GameMaster.loggit(f"""{player.icon} tripped.""")

                player.recordLoss()
                self.spawnPlayer(player)

            # did player hit exit
            if player_tile_type == MapData.EMOJI["SAVED"]:
                self.newGame()
                print(player.conn, "WON")

                GameMaster.loggit(f"""{player.icon} wins!""")

            # did player hit enemy
            for entity in EntityData.all_instances:
                if player.position == entity.position:
                    player.recordLoss()
                    self.spawnEntity(entity)
                    self.spawnPlayer(player)

                    # log
                    print(datetime.now(), player.conn,
                          "hits", entity.icon, "#", player.loss_numb)
                    GameMaster.loggit(
                        f"""{entity.icon} > {player.icon}; #{player.loss_numb}""")

    async def gameLoop(self):
        """Coroutine to execute main game loop logic"""

        last_move_time = time.time()

        while True:

            # MOVE ENTITIES

            # move entities each second
            current_time = time.time()
            if current_time - last_move_time >= .5:
                self.moveAllEntities()
                last_move_time = current_time

            # is game over
            self.gameOver()

            # update display, for now
            self.updateFramebuffer()

            # game loop speed
            await asyncio.sleep(.05)

    def newGame(self):
        """Function to make new game while network is active."""

        # reset game log
        GameMaster.log = []
        GameMaster.game_time = datetime.now()

        # make a new map
        self.MapData = MapData(GAMESIZE=GameMaster.GAMESIZE,
                               EDGESIZE=GameMaster.EDGESIZE)

        # reset game map and framebuffer
        self.gamemap = tuple(self.MapData.tilemap)
        self.framebuffer = list(self.gamemap)

        # reset player positions
        for player in PlayerData.all_instances:
            self.spawnPlayer(player)

        # reset existing entities
        EntityData.all_instances = []
        self.createEntities()
        self.spawnInitial()

        # count resets
        GameMaster.game_numb += 1
        GameMaster.loggit(f"""NEW GAME! #{self.game_numb}""")


class ComMan:
    """Class for a server control interface."""

    def __init__(self, game_master_inst):
        self.game = game_master_inst
        pass

    async def commLoop(self):  # Asynchronous main loop
        """Server control interface mainloop using asynchronous input."""
        while True:
            clear()
            print("Menu")
            print("  1 - Show All Players ")
            print("  2 - Live Framebuffer")
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
                the_game.showFramebuffer()

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

            # ... (handle other choices similarly)

            elif choice == 9:
                clear()
                LogMe.saveText()
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

    def __init__(self, ADDR, PORT) -> None:
        self.network_addr = ADDR
        self.admin_port = PORT
        self.server = None

    async def handle_connection(self, websocket, path):
        """Handles incoming connections from admin clients and sends updates."""

        while True:
            try:
                # datas to send
                await self.sendEntityData(websocket)
                await self.sendFramebuffer(websocket)
                await self.sendLogData(websocket)
                await self.sendPlayerData(websocket)
                await self.sendServerStatus(websocket)

                # delay
                await asyncio.sleep(1)

            except websockets.ConnectionClosed:

                print(f"""{datetime.now()} {
                      websocket.remote_address} admin: disconnected.""")
                break

    async def sendFramebuffer(self, websocket):
        framebuffer = the_game.framebuffer
        await websocket.send(
            json.dumps({"type": "framebuffer", "data": framebuffer})
        )

    async def sendEntityData(self, websocket):
        """Function to get and send entity data to web page"""
        entity_data_list = []

        for entity in EntityData.all_instances:
            entity_data_list.append({
                "serial": f"{entity.unique_id:04d}",
                "icon": f"{entity.icon}",
                "indx": f"{entity.position:06d}",
                "move": f"{entity.move_numb:06d}",
                "xypo": f"{entity.getXYFromIndex(GameMaster.GAMESIZE)}"
            })

        await websocket.send(json.dumps({
            "type": "entity_data_update",
            "data": entity_data_list
        }))

    async def sendLogData(self, websocket):
        """Function to send game's log data to web page."""

        # get log
        log_data = GameMaster.log

        await websocket.send(json.dumps({
            "type": "log_data",
            "data": log_data
        }))

    async def sendPlayerData(self, websocket):
        """Function to get and send player data/ view to web page"""
        player_data_list = []
        for player in PlayerData.all_instances:
            player_data_list.append({
                "addr": player.conn[0],
                "icon": player.icon,
                "indx": player.position,
                "move": player.move_numb,
                "time": player.getTimeOnline(),
                "view": the_game.getPlayerView(player)
            })

        await websocket.send(json.dumps({
            "type": "player_data_update",
            "data": player_data_list
        }))

    async def sendServerStatus(self, websocket):
        """Function to get and send both server-uptime and users-online to web page"""
        system_cpu, system_ram = monitor_server_load()
        uptime = GameMaster.getUptime()
        users_online = len(PlayerData.all_instances)
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

        self.server = await websockets.serve(
            self.handle_connection, self.network_addr, self.admin_port
        )

        # SSL ON
        # self.server = await websockets.serve(
        #     self.handle_connection, self.network_addr, self.admin_port, ssl=ssl_context)


class ClientServer:

    clients = set()
    client_history = []

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

        # start tasks: sending (game data) & receiving (input)
        await asyncio.gather(
            self.send_task(websocket, new_player),
            self.receive_task(websocket, new_player)
        )

        # remove player on disconnect
        print(datetime.now(), new_player.conn, "player: disconnected.")
        GameMaster.loggit(f"""{new_player.icon} disconnected.""")
        ClientServer.clients.remove(websocket)
        PlayerData.all_instances.remove(new_player)

    async def send_task(self, websocket, player):
        """Sends game state updates to the client."""
        while True:
            try:
                game_board = self.game.getPlayerView(player)
                await websocket.send(json.dumps({"type": "gameState", "data": game_board}))

                # send users online
                users_online = len(PlayerData.all_instances)
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
                        print(f"""{datetime.now()} {
                              player.conn} Input rate exceeded ({player_input})""")
            except websockets.ConnectionClosed:
                break

    async def mainLoop(self):
        # SSL OFF
        return await websockets.serve(self.handle_connection, self.ADDR, self.PORT)

        # SSL ON
        # return await websockets.serve(self.handle_connection, self.ADDR, self.PORT, ssl=ssl_context)

################################################################################
# EXECUTION
################################################################################


async def main():
    # LOGGING
    logman = LogMe()

    # network data
    ADDR = "0.0.0.0"
    PORT_CLNT = 5002
    PORT_ADMN = 5003

    # temp fix
    global the_game

    # make game world
    the_game = GameMaster()
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
    the_admin_server = AdminServer(ADDR, PORT_ADMN)
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
