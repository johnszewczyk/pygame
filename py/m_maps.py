'''Module for tile map generation'''

import copy
import math
import random

from datetime import datetime

from m_cabins import *
from m_icons import *
from m_shapes import *
from m_tiles import *


# TILE MAP GENERATOR
# ------------------------------------------------------------------------------


# sloppy hopper for Tiles


class TileLand:
    '''Sloppy hopper class for Tiles'''

    TILE_RATE = [
        (CabinsTile, 0.2),
        (FieldsTile, 2.0),
        (RocksTile, 1.0),
        (TreesTile, 5.0),
        (WatersTile, 0.2),
        (WoodsTile, 50),
        (WrecksTile, 1.0),
    ]

    ICON_TO_TILE_CLASS = {
        EMOJI['CABIN']: CabinsTile,
        EMOJI['DOOR']: DoorsTile,
        EMOJI['GRAVE']: GravesTile,
        EMOJI['LINK']: LinksTile,
        EMOJI['ROCK']: RocksTile,
        EMOJI['TREE']: TreesTile,
        EMOJI['WATER']: WatersTile,
        EMOJI['WOODS']: WoodsTile,
        EMOJI['WRECKED']: WrecksTile,
    }

    def __init__(self, game_size, edge_size) -> None:
        # args
        self.game_size = game_size
        self.edge_size = edge_size

        # calc tile grid
        self.GRID = {
            "NE": self.edge_size * self.game_size - self.edge_size + self.game_size - 1,
            "NW": self.game_size * self.edge_size + self.edge_size,
            "SE": self.game_size * self.game_size - self.edge_size * self.game_size - self.edge_size - 1,
            "SW": self.game_size * self.game_size - self.edge_size * self.game_size + self.edge_size - self.game_size,
        }

        # vars
        self.grid_size = self.game_size * self.game_size

        # make global
        Tiles.classReset()
        Tiles.edge_size = edge_size
        Tiles.game_size = game_size
        Tiles.GRID = self.GRID

        # make game map
        self.makeLand()

    def drawRect(self, index, wide, deep, value, direction):
        '''Function to draw a rectangle of [value] from [index] on self-map'''

        # Error handling for invalid directions
        if direction not in ["downright", "upleft", "upright", "downleft"]:
            print(
                "Invalid direction. Please use downright, upleft, upright, or downleft.")
            return

        # Calculate offsets based on direction
        w_offset = 1  # Default offset for width (right)
        h_offset = self.game_size  # Default offset for height (down)

        if "up" in direction:
            h_offset *= -1  # Multiply by -1 for upward directions
        if "left" in direction:
            w_offset *= -1  # Multiply by -1 for leftward directions

        # Draw the rectangle
        for w in range(wide):
            position = index + w * w_offset
            for h in range(deep):
                newindex = position + h * h_offset

                # save to tile grid
                Tiles.all_insts[newindex] = value(newindex, init_flag=False)

    def edgeDetect(self, index):
        '''Function to detect and set edge-class tiles'''

        x = index % self.game_size
        y = index // self.game_size

        is_edge = (x < self.edge_size or x >= (self.game_size - self.edge_size) or
                   y < self.edge_size or y >= (self.game_size - self.edge_size))
        return is_edge

    def makeLand(self):
        '''Function to populate array randomly using tile classes'''

        # wipe data
        Tiles.classReset()

        # tell Tiles class the map size data
        self.game_size = self.game_size
        self.edge_size = self.edge_size

        # make tiles in loop
        for index in range(self.grid_size):

            # generate tile type
            tile_class, _ = random.choices(
                TileLand.TILE_RATE,
                weights=[weight for _, weight in TileLand.TILE_RATE], k=1)[0]

            # make init tile inst
            init_flag = True

            # make edge tile if edge
            if self.edgeDetect(index):
                # if edge, make next tile edge-type
                next_tile = EdgesTile(index, init_flag)
            else:
                # make random tile
                next_tile = tile_class(index, init_flag)

        # draw shapes on map - auto
        pencil = ShapeMaker(self.game_size)
        pencil.populateShapes()

        print("MAP GENERATED")


# TILE MAP SHAPE MAKER
# ------------------------------------------------------------------------------


class ShapeMaker:

    used_indices = []

    def __init__(self, game_size):
        self.game_size = game_size

    def doesShapeFit(self, root_index, shape):
        """Function to test for edge or other shape @ [root_index] for [shape]"""

        # print("DOES SHAPE FIT")

        # get size of square monument via square root
        dimension = math.sqrt(len(shape))
        dimension = int(dimension)

        deep = dimension
        wide = dimension

        for x_offset in range(wide):
            position = root_index + x_offset

            for y_offset in range(deep):
                new_index = position + y_offset * self.game_size

                # print(f"SHAPEFIT: {new_index}; {wide}{deep}")

                # don't draw monument if it extends beyond edge
                selected_tile = Tiles.all_insts[new_index]

                # print(f"  EDGE: {selected_tile.tile_edge}")

                if selected_tile.tile_edge:
                    # print("  fail: edge tile")
                    return False

                # don't draw if it overlaps another shape
                if new_index in ShapeMaker.used_indices:
                    print("  fail: other shape")
                    return False
        # print(f"  SHAPE FITS")
        return True

    def drawShape(self, root_tile, shape):
        """Function to draw shape at position using Tile instances."""

        # Get the root index from the root_tile
        root_index = root_tile.tile_index

        # print("DRAW SHAPE @ ", root_index)

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

            # Create the appropriate tile instance based on the icon
            tile_class = TileLand.ICON_TO_TILE_CLASS.get(tile_icon)
            if tile_class:
                new_tile = tile_class(index, init_flag=False)
            else:
                print(f"ERROR: undef: {tile_icon}.")

            # replace the tile; removing first will make gaps
            Tiles.all_insts[index] = new_tile

            # save index of shape-type tiles
            ShapeMaker.used_indices.append(index)

            # Increment position - horizontal
            x_offset += 1

            # Increment position - vertical
            if x_offset == dimension:
                x_offset = 0
                y_offset += self.game_size

            # print("  DRAW TILE @", loop_iter, "of", len(shape),
            #       new_tile.tile_index, new_tile.tile_icon)

    def populateShapes(self):
        """Function to draw all predefined shapes to map using other funcs"""

        # CABINS
        loop_iter = 0
        root_tiles = copy.deepcopy(CabinsTile.all_insts)
        for tile in root_tiles:
            loop_iter += 1

            # pick shape
            shape = Cabins.someCabin()

            # does shape fit
            if self.doesShapeFit(tile.tile_index, shape):
                # draw shape [index] [shape]
                self.drawShape(tile, shape)

        # MONUMENTS
        loop_iter = 0
        root_tiles = copy.deepcopy(WatersTile.all_insts)
        for tile in root_tiles:
            loop_iter += 1

            # pick shape
            shape = Monuments.someMonument()
            # print(shape)

            # does shape fit
            if self.doesShapeFit(tile.tile_index, shape):
                # draw shape [index] [shape]
                self.drawShape(tile, shape)
