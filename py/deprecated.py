'''Deprecated content'''

# MAP
# ------------------------------------------------------------------------------


# class MapData:


# # directional offsets
# self.PATH_N = -self.GAMESIZE
# self.PATH_S = self.GAMESIZE
# self.PATH_E = 1
# self.PATH_W = -1
# self.PATH_NE = -self.GAMESIZE + 1
# self.PATH_NW = -self.GAMESIZE - 1
# self.PATH_SE = self.GAMESIZE + 1
# self.PATH_SW = self.GAMESIZE - 1

#     @staticmethod
#     def getDimensions(shape):
#         """Function to calc dimensions of shape in string-type variable."""
#         shape = shape.strip()

#         # Initialize width counter
#         width = 0

#         # get width
#         for char in shape.splitlines():
#             if char != '\n':  # Check if character is not a newline
#                 width += 1
#             else:
#                 break

#         # get height
#         height = len(shape.splitlines())

#         return width, height

#     def exportTextFile(self):
#         """Write tile map to .txt file in path."""

#         date_str = datetime.now().strftime("%y%m%d-%H:%M:%S.%f")
#         filename = f"{date_str}_emojimap.txt"

#         # Open the file for writing in text mode
#         with open(filename, 'w') as file:
#             # Need array dimension to write lines
#             size = len(self.emojimap)
#             size = math.sqrt(size)
#             size = int(size)

#             # Write each tile to the file
#             for line in range(size):
#                 for item in self.emojimap[line * size:(line + 1) * size]:
#                     file.write(item)
#                 # Add a newline character at the end of each line
#                 file.write('\n')


#     def isFloorTile(self, index):
#         """Checks if a cabin tile is a floor tile (surrounded by cabin or door tiles)."""
#         if self.emojimap[index] != MapData.EMOJI["CABIN"]:
#             return False

#         for offset in self.COMPASS_8:
#             # Check for neighbors that are not walls or doors, which would make it a floor
#             if self.emojimap[index + offset] not in (MapData.EMOJI["CABIN"], MapData.EMOJI["DOOR"]):
#                 return False
#         return True

#     def isWallTile(self, index):
#         """Checks if a cabin tile is a wall tile (adjacent to a non-cabin tile)."""
#         if self.emojimap[index] != MapData.EMOJI["CABIN"]:
#             return False

#         for offset in self.COMPASS_8:
#             # Check for at least one neighbor that is not a cabin tile
#             if self.emojimap[index + offset] not in [MapData.EMOJI["CABIN"], MapData.EMOJI["DOOR"]]:
#                 return True
#         return False

#     def echoTileMap(self):
#         """Draw tile map to terminal"""

#         # need array dimension to draw lines
#         size = len(self.emojimap)
#         size = math.sqrt(size)

#         print()

#         line = 0
#         for item in self.emojimap:
#             line += 1
#             print(item, end='')
#             if line == size:
#                 line = 0
#                 print('')


#     def drawRect(self, index, wide, deep, value):
#         '''Function to draw a rectangle of [value] from [index] on self-map'''

#         # test area for edge; stop draw if object extends to edge tile

#         for w in range(wide):
#             position = index + w

#             # for height...
#             for h in range(deep):
#                 new_index = position + h * self.GAMESIZE

#                 if self.isEdgeIndex(new_index):
#                     return

#         # calculate positions and write

#         # for width...
#         for w in range(wide):
#             position = index + w

#             # for height...
#             for h in range(deep):
#                 new_index = position + h * self.GAMESIZE

#                 # draw tile
#                 self.emojimap[new_index] = value

#                 # # draw tile
#                 # if not self.isEdgeIndex(new_index):
#                 #     self.emojimap[new_index] = value


# def __init__(self, GAMESIZE, EDGESIZE):
#     '''Make game map'''

#     # save instances
#     MapData.all_calls += 1
#     MapData.all_instances.append(self)

#     # instace vars
#     self.GAMESIZE = GAMESIZE
#     self.EDGESIZE = EDGESIZE

#     # tile lists
#     self.emojimap = []
#     self.tilelist_cabin = []
#     self.tilelist_water = []
#     self.tilelist_woods = []

#     self.all_shapes = []

#     self.tilelist_block = ()

#     # # grid tile positions
#     # self.GRID_NE = EDGESIZE * GAMESIZE - EDGESIZE + GAMESIZE - 1
#     # self.GRID_NW = GAMESIZE * EDGESIZE + EDGESIZE
#     # self.GRID_SE = GAMESIZE * GAMESIZE - EDGESIZE * GAMESIZE - EDGESIZE - 1
#     # self.GRID_SW = GAMESIZE * GAMESIZE - EDGESIZE * GAMESIZE + EDGESIZE - GAMESIZE

#     # # directional offsets
#     # self.PATH_N = -GAMESIZE
#     # self.PATH_S = GAMESIZE
#     # self.PATH_E = 1
#     # self.PATH_W = -1
#     # self.PATH_NE = -GAMESIZE + 1
#     # self.PATH_NW = -GAMESIZE - 1
#     # self.PATH_SE = GAMESIZE + 1
#     # self.PATH_SW = GAMESIZE - 1

#     # # directional groups
#     # self.COMPASS_8 = [self.PATH_N,
#     #                   self.PATH_S,
#     #                   self.PATH_E,
#     #                   self.PATH_W,
#     #                   self.PATH_NW,
#     #                   self.PATH_NE,
#     #                   self.PATH_SW,
#     #                   self.PATH_SE]
#     # self.COMPASS_4 = [self.PATH_N,
#     #                   self.PATH_S,
#     #                   self.PATH_E,
#     #                   self.PATH_W]
#     # self.COMPASS_X = [self.PATH_NW,
#     #                   self.PATH_NE,
#     #                   self.PATH_SW,
#     #                   self.PATH_SE]


#     # make some tiles manually
#     # self.emojimap[self.GRID_NE] = MapData.EMOJI['SAVED']
#     # self.emojimap[self.GRID_NW] = MapData.EMOJI['WRECKED']

#     # make some tiles manually - add doors to safe spawn
#     # self.emojimap[self.GRID_SW + 3] = MapData.EMOJI['DOOR']
#     # self.emojimap[self.GRID_SW - (GAMESIZE * 3)] = MapData.EMOJI['DOOR']

#     # save map to disk
#     # self.exportTextFile()
