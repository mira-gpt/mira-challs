from gdo.core.GDT_Object import GDT_Object
from gdo.mira_challs.GDO_Challenge import GDO_Challenge


class GDT_Challenge(GDT_Object):
    def __init__(self, name):
        super().__init__(name)
        self.table(GDO_Challenge.table())
