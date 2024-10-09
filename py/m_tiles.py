'''Module for tile properties'''


import copy


from datetime import datetime


# TILE META
# ------------------------------------------------------------------------------


class TileMeta(type):
    '''
    Metaclass for creating Tile subclasses with shared properties.
    '''

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

# TILE PROPERTIES
# ------------------------------------------------------------------------------


class Tiles(metaclass=TileMeta):
    '''Parent class for all tile types'''

    # game_size = None
    # EDGESIZE = None

    def __init__(self, tile_index, init_flag) -> None:
        '''Initialize standard tile properties'''

        # Append to all_insts only during initial creation
        if init_flag:
            Tiles.all_insts.append(self)

        Tiles.all_calls += 1
        # Tiles.all_insts.append(self)

        # args
        self.tile_index = tile_index  # permanent index

        # vars - identity
        self.tile_edge = None  # edge-type tile
        self.tile_exit = None  # exit-type tile
        self.tile_icon = None  # base tile view
        self.tile_icon_from_interior = None  # alt. tile view
        self.tile_icon_from_exterior = None  # alt. tile view

        self.tile_roof = False  # roof obscures entities
        self.tile_objc_list = []  # list of class objects inhabting tile

        # vars - data
        self.tile_last_used = None  # save last date
        self.tile_last_user = None  # save last user
        self.tile_user = None  # save unit on tile
        self.tile_uses = []  # save uses date
        self.tile_user_icon = set()  # save unique visitor list of emoji
        self.tile_user_list = set()  # save unique visitor list of object

        # vars - pass
        self.tile_link = []  # list of tiles with linked access
        self.tile_access = False
        self.tile_access_entity = False
        self.tile_access_player = False

        self.tile_trap = None  # trap/ loss tile
        self.tile_trap_text = None  # trap/ loss text
        self.tile_unique_id = copy.deepcopy(Tiles.all_calls)

        self.tile_wall = None

        # setters
        self.tile_posx = None  # set at init
        self.tile_posy = None  # set at init
        self.setPosXY()

    @classmethod
    def classReset(cls):
        '''Function to reset subclass class-level vars'''
        Tiles.all_calls = 0
        Tiles.all_insts = []

        for subclass in cls.__subclasses__():
            subclass.all_calls = 0
            subclass.all_insts = []

    @property
    def lastUsed(self):
        '''Function/ Property to calculate time elapsed since last used'''
        if self.tile_last_used:
            # Directly subtract datetime objects
            time_diff = datetime.now() - self.tile_last_used
            days = time_diff.days
            hours, remainder = divmod(time_diff.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)

            return f'{days:02d}:{hours:02d}:{minutes:02d}:{seconds:02d} ago'
        else:
            return 'Never'

    @property
    def uniqUsed(self):
        '''Function/ Property to calculate length of all users set'''
        return len(self.tile_user_list)

    def setPosXY(self):
        '''Function to make (X,Y) from index position and game size'''
        self.tile_posx = self.tile_index % Tiles.game_size
        self.tile_posy = self.tile_index // Tiles.game_size

    def setFloorTile(self):
        '''Function to flag interior tile with no adjacent exterior tiles'''
        pass


# TILE PROPERTIES - SUB CLASSES
# ------------------------------------------------------------------------------


class CabinsTile(Tiles):

    def __init__(self, tile_index, init_flag):
        super().__init__(tile_index, init_flag)

        self.tile_icon = '🏠'
        self.tile_icon_from_exterior = '🏠'

        # movement vars
        self.tile_access = True
        self.tile_access_entity = False
        self.tile_link = [CabinsTile, DoorsTile]
        self.tile_roof = True


class DoorsTile(Tiles):

    def __init__(self, tile_index, init_flag):
        super().__init__(tile_index, init_flag)

        self.tile_icon = '🚪'
        self.tile_access = True
        self.tile_access_entity = True
        self.tile_link = [CabinsTile, DoorsTile]


class EdgesTile(Tiles):

    def __init__(self, tile_index, init_flag):
        super().__init__(tile_index, init_flag)

        self.tile_icon = '🌳'
        self.tile_access = False
        self.tile_edge = True


class ExitsTile(Tiles):

    def __init__(self, tile_index, init_flag):
        super().__init__(tile_index, init_flag)

        self.tile_icon = '🚔'
        self.tile_access = True
        self.tile_access_entity = False


class FieldsTile(Tiles):

    def __init__(self, tile_index, init_flag):
        super().__init__(tile_index, init_flag)
        # FieldsTile.all_calls += 1
        # FieldsTile.all_insts.append(self)

        self.tile_icon = '🌾'
        self.tile_icon_from_interior = '⬛️'
        self.tile_is_exterior = True
        self.tile_is_interior = False
        self.tile_access = True


class GravesTile(Tiles):

    def __init__(self, tile_index, init_flag):
        super().__init__(tile_index, init_flag)

        self.tile_icon = '🪦'
        self.tile_icon_from_interior = '⬛️'
        self.tile_is_exterior = True
        self.tile_is_interior = False


class LinksTile(Tiles):

    def __init__(self, tile_index, init_flag):
        super().__init__(tile_index, init_flag)

        self.tile_icon = '🔗'
        # self.tile_icon_from_interior = '⬛️'
        self.tile_is_exterior = True
        self.tile_is_interior = False


class RocksTile(Tiles):

    def __init__(self, tile_index, init_flag):
        super().__init__(tile_index, init_flag)

        self.tile_icon = '🪨'
        self.tile_access = True
        self.tile_access_entity = True
        self.tile_access_player = False
        self.tile_is_exterior = True
        self.tile_is_interior = False
        self.tile_roof = True


class TreesTile(Tiles):

    def __init__(self, tile_index, init_flag):
        super().__init__(tile_index, init_flag)

        self.tile_icon = '🌳'
        self.tile_icon_from_interior = '⬛️'
        self.tile_name = 'trees'
        self.tile_access = False
        self.tile_access_entity = True


class WatersTile(Tiles):

    def __init__(self, tile_index, init_flag):
        super().__init__(tile_index, init_flag)

        self.tile_icon = '🌊'
        self.tile_is_exterior = True
        self.tile_is_interior = False
        self.tile_access = True
        self.tile_trap = True
        self.tile_trap_text = 'drowned.'


class WoodsTile(Tiles):

    def __init__(self, tile_index, init_flag):
        super().__init__(tile_index, init_flag)

        self.tile_icon = '🌲'
        self.tile_icon_from_interior = '⬛️'
        self.tile_is_exterior = True
        self.tile_is_interior = False
        self.tile_access = True


class WrecksTile(Tiles):

    def __init__(self, tile_index, init_flag):
        super().__init__(tile_index, init_flag)

        self.tile_icon = '🏚️'
        self.tile_access = True
        self.tile_roof = True
        self.tile_trap = True
        self.tile_trap_text = 'fell.'
