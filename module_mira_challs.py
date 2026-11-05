from gdo.base.GDO_Module import GDO_Module
from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.mira_challs.GDO_ChallengeSolved import GDO_ChallengeSolved


class module_mira_challs(GDO_Module):
    """PyGDO module for Mira's challenge site."""

    def gdo_classes(self):
        return [GDO_Challenge, GDO_ChallengeSolved]
