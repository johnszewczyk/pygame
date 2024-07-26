
class EntityData:

    """Class to manage all non-human entities"""

    EMOJI = {}
    EMOJI["KNIFE"] = "🔪"
    EMOJI["WOLF"] = "🐺"
    EMOJI["SPIDER"] = "🕷️"

    all_calls = 0
    all_instances = []

    def __init__(self, icon, movetype, index, hometile):

        # save instance data
        EntityData.all_calls += 1
        EntityData.all_instances.append(self)

        # args
        self.icon = icon
        self.movetype = movetype
        self.position = index
        self.hometile = hometile

        # vars
        self.last_pos = self.position
        self.move_none = 0
        self.move_numb = 0
        self.move_rate = 0
        self.same_tile = 0
        self.unique_id = EntityData.all_calls

    @staticmethod
    def factory(quantity, icon, movetype, index, hometile):
        for i in range(quantity):
            inst = EntityData(
                icon=icon,
                movetype=movetype,
                index=index,
                hometile=hometile,
            )

    @classmethod
    def getEntityIndices(cls):
        """Return all entity location indices"""
        return (entity.position for entity in cls.all_instances)

    @classmethod
    def showAll(cls):
        """Print all instances of Entities class, formatted to grid"""

        line = 0
        char = 8
        for entity in cls.all_instances:
            line += 1
            print(f"{entity.icon}:"
                  f"{entity.serial:0{4}}:"
                  f"{entity.position:0{4}}", end="")

            if line > char:
                line = 0
                print()

    def getXYFromIndex(self, dimension):
        """Function to convert from POSITION to X,Y"""
        x = self.position % dimension
        y = self.position // dimension
        return x, y
