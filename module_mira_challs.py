from gdo.base.GDO_Module import GDO_Module
from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.mira_challs.GDO_ChallengeSolved import GDO_ChallengeSolved
from gdo.ui.GDT_Link import GDT_Link


class module_mira_challs(GDO_Module):
    """PyGDO module for Mira's challenge site."""

    def gdo_classes(self):
        return [GDO_Challenge, GDO_ChallengeSolved]

    def gdo_init_sidebar(self, page):
        page._left_bar.add_field(GDT_Link().href(self.href('overview')).text('module_mira_challs'))
