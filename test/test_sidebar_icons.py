import unittest
from unittest.mock import MagicMock, patch

from gdo.mira_challs.module_mira_challs import module_mira_challs


class SidebarIconsTest(unittest.TestCase):
    def test_challenges_welcome_and_ranking_use_trophy(self):
        page = MagicMock()
        module = module_mira_challs()
        with patch.object(module_mira_challs, 'href', side_effect=lambda name: '/' + name), \
             patch('gdo.base.Application.Application.get_mode', return_value=None):
            module.gdo_init_sidebar(page)
        links = [call.args[0] for call in page._left_bar.add_field.call_args_list]
        self.assertEqual(['trophy', 'trophy', 'trophy'], [link._icon_name for link in links])
        self.assertEqual(['/welcome', '/ranking', '/challenges'], [link._href for link in links])
