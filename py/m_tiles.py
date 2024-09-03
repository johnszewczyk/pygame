# TILE PROPERTIES
# ------------------------------------------------------------------------------


class Tiles:
    all_calls = 0
    all_insts = []

    GAMESIZE = None
    EDGESIZE = None

    def __init__(self, tile_posi, init_flag) -> None:

        # Append to all_insts only during initial creation
        if init_flag:
            Tiles.all_insts.append(self)

        Tiles.all_calls += 1
        # Tiles.all_insts.append(self)

        # args
        self.tile_posi = tile_posi

        # vars
        self.tile_edge = None
        self.tile_exit = None
        self.tile_icon = None
        self.tile_type = None
        self.tile_view = None
        self.tile_view_alt = None
        self.tile_view_outside = True
        self.tile_view_inside = True
        self.tile_last_pass = None
        self.tile_last_char = None
        self.tile_last_time = None
        self.tile_link = None
        self.tile_lock = None
        self.tile_name = None
        self.tile_pass = False
        self.tile_pass_entity = False
        self.tile_pass_player = False
        self.tile_posx = None
        self.tile_posy = None
        self.tile_trap = False
        self.tile_trap_text = None

        # setters
        self.setPosXY()

        print("NEW TILE #", Tiles.all_calls, "@", self.tile_posi)

    def setEdge(self):
        '''Function to determine if tile is on the edge of the map'''

        x = self.tile_posi % Tiles.GAMESIZE
        y = self.tile_posi // Tiles.GAMESIZE

        is_edge = (x < Tiles.EDGESIZE or x >= (Tiles.GAMESIZE - Tiles.EDGESIZE) or
                   y < Tiles.EDGESIZE or y >= (Tiles.GAMESIZE - Tiles.EDGESIZE))

        self.tile_edge = is_edge
        if self.tile_edge:
            self.tile_icon = "🌳"

    def setPosXY(self):
        '''Function to make (X,Y) from index position and game size'''
        self.tile_posx = self.tile_posi % Tiles.GAMESIZE
        self.tile_posy = self.tile_posi // Tiles.GAMESIZE


# TILE PROPERTIES - SUB CLASSES
# ------------------------------------------------------------------------------


class CabinsTile(Tiles):
    all_calls = 0
    all_insts = []

    def __init__(self, tile_posi, init_flag):
        super().__init__(tile_posi, init_flag)
        CabinsTile.all_calls += 1
        CabinsTile.all_insts.append(self)

        self.tile_icon = "🏠"
        self.tile_name = "cabin"

        self.tile_exit = False
        self.tile_pass = True
        self.tile_pass_entity = False
        self.tile_link = ["cabin", "door"]


class DoorsTile(Tiles):
    all_calls = 0
    all_insts = []

    def __init__(self, tile_posi, init_flag):
        super().__init__(tile_posi, init_flag)
        DoorsTile.all_calls += 1
        DoorsTile.all_insts.append(self)

        self.tile_icon = "🚪"
        self.tile_name = "door"
        self.tile_pass = True
        self.tile_pass_entity = True
        self.tile_link = ["cabin", "door"]


class FieldsTile(Tiles):
    all_calls = 0
    all_insts = []

    def __init__(self, tile_posi, init_flag):
        super().__init__(tile_posi, init_flag)
        FieldsTile.all_calls += 1
        FieldsTile.all_insts.append(self)

        self.tile_icon = "🌾"
        self.tile_name = "field"
        self.tile_pass = True


class FloorsTile(Tiles):
    all_calls = 0
    all_insts = []

    def __init__(self, tile_posi, init_flag):
        super().__init__(tile_posi, init_flag)
        FloorsTile.all_calls += 1
        FloorsTile.all_insts.append(self)

        self.tile_icon = "⬛️"
        self.tile_name = "floor"
        self.tile_pass = True


class RocksTile(Tiles):
    all_calls = 0
    all_insts = []

    def __init__(self, tile_posi, init_flag):
        super().__init__(tile_posi, init_flag)
        RocksTile.all_calls += 1
        RocksTile.all_insts.append(self)

        self.tile_icon = "🪨"
        self.tile_name = "boulder"


class TreesTile(Tiles):
    all_calls = 0
    all_insts = []

    def __init__(self, tile_posi, init_flag):
        super().__init__(tile_posi, init_flag)
        TreesTile.all_calls += 1
        TreesTile.all_insts.append(self)

        self.tile_icon = "🌳"
        self.tile_name = "trees"
        self.tile_pass = False


class WatersTile(Tiles):
    all_calls = 0
    all_insts = []

    def __init__(self, tile_posi, init_flag):
        super().__init__(tile_posi, init_flag)
        WatersTile.all_calls += 1
        WatersTile.all_insts.append(self)

        self.tile_icon = "🌊"
        self.tile_name = "water"
        self.tile_pass = True
        self.tile_trap = True
        self.tile_trap_text = "drowned."


class WoodsTile(Tiles):
    all_calls = 0
    all_insts = []

    def __init__(self, tile_posi, init_flag):
        super().__init__(tile_posi, init_flag)
        WoodsTile.all_calls += 1
        WoodsTile.all_insts.append(self)

        self.tile_icon = "🌲"
        self.tile_name = "woods"
        self.tile_pass = True


class WreckedTile(Tiles):
    all_calls = 0
    all_insts = []

    def __init__(self, tile_posi, init_flag):
        super().__init__(tile_posi, init_flag)
        WoodsTile.all_calls += 1
        WoodsTile.all_insts.append(self)

        self.tile_icon = "🏚️"
        self.tile_name = "wrecked"
        self.tile_pass = True
        self.tile_trap = True
        self.tile_trap_text = "fell."
