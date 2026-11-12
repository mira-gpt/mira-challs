from gdo.base.GDO_Module import GDO_Module
from gdo.core.GDT_Bool import GDT_Bool
from gdo.core.GDT_Password import GDT_Password
from gdo.country.GDT_Country import GDT_Country
from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.mira_challs.GDO_ChallengeSolved import GDO_ChallengeSolved
from gdo.ui.GDT_Link import GDT_Link


class module_mira_challs(GDO_Module):
    """PyGDO module for Mira's challenge site."""

    def gdo_dependencies(self) -> list[str]:
        return ['country']

    def gdo_user_settings(self):
        return [GDT_Country('country_of_scoring').tooltip('tt_country_of_scoring')]

    def gdo_module_config(self):
        return [
            GDT_Bool('wechall_enabled').not_null().initial('0'),
            GDT_Password('wechall_authkey'),
        ]

    def gdo_classes(self):
        return [GDO_Challenge, GDO_ChallengeSolved]

    def gdo_main_method_name(self):
        return 'welcome'

    def gdo_admin_links(self) -> list[GDT_Link]:
        return [
            GDT_Link().href(self.href('install')).text('mt_mira_challs_install'),
        ]

    def gdo_init_sidebar(self, page):
        page._left_bar.add_field(GDT_Link().href(self.href('welcome')).text('module_mira_challs'))
        page._left_bar.add_field(GDT_Link().href(self.href('ranking')).text('mt_mira_challs_ranking'))
