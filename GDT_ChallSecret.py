from gdo.core.GDT_Password import GDT_Password


class GDT_ChallSecret(GDT_Password):
    def __init__(self, name):
        super().__init__(name)
        self.minlen(1)
