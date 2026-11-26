from gdo.base.GDO_Module import GDO_Module
from gdo.base.Application import Application
from gdo.core.GDT_Bool import GDT_Bool
from gdo.core.GDT_Password import GDT_Password
from gdo.country.GDT_Country import GDT_Country
from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.mira_challs.GDO_ChallengeSolved import GDO_ChallengeSolved
from gdo.mira_challs.GDO_ChallengeSolution import GDO_ChallengeSolution
from gdo.mira_challs.GDO_ChallengeTag import GDO_ChallengeTag
from gdo.mira_challs.GDO_ChallengeTagLink import GDO_ChallengeTagLink
from gdo.ui.GDT_Link import GDT_Link


class module_mira_challs(GDO_Module):
    """PyGDO module for Mira's challenge site."""

    def __init__(self):
        super().__init__()
        self._priority = 51

    def gdo_dependencies(self) -> list[str]:
        return ['country', 'tags', 'markdown', 'forum']

    def gdo_user_settings(self):
        return [GDT_Country('country_of_scoring').tooltip('tt_country_of_scoring')]

    def gdo_module_config(self):
        return [
            GDT_Bool('wechall_enabled').not_null().initial('0'),
            GDT_Password('wechall_authkey'),
            GDT_Bool('show_intro_link').not_null().initial(
                '1' if Application.config('core.main_module', 'core') == 'mira_challs' else '0'
            ).tooltip('tt_mira_challs_show_intro_link'),
        ]

    def gdo_classes(self):
        return [GDO_Challenge, GDO_ChallengeSolved, GDO_ChallengeSolution, GDO_ChallengeTag, GDO_ChallengeTagLink]

    def gdo_main_method_name(self):
        return 'welcome'

    def gdo_admin_links(self) -> list[GDT_Link]:
        return [
            GDT_Link().href(self.href('install')).text('mt_mira_challs_install'),
        ]

    def gdo_init_sidebar(self, page):
        if self.get_config_value('show_intro_link'):
            page._left_bar.add_field(GDT_Link().href(self.href('welcome')).text('module_mira_challs').icon('trophy'))
        page._left_bar.add_field(GDT_Link().href(self.href('challenges')).text('mira_challs_sidebar_challenges').icon('trophy'))
        page._left_bar.add_field(GDT_Link().href(self.href('ranking')).text('mt_mira_challs_ranking').icon('trophy'))
