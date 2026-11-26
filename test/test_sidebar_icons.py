import unittest
from unittest.mock import MagicMock, patch

from gdo.mira_challs.module_mira_challs import module_mira_challs


class SidebarIconsTest(unittest.TestCase):
    def test_challenges_welcome_and_ranking_use_trophy(self):
        page = MagicMock()
        module = module_mira_challs()
        with patch.object(module_mira_challs, 'href', side_effect=lambda name: '/' + name), \
             patch.object(module, 'get_config_value', return_value=True), \
             patch('gdo.base.Application.Application.get_mode', return_value=None):
            module.gdo_init_sidebar(page)
        links = [call.args[0] for call in page._left_bar.add_field.call_args_list]
        self.assertEqual(['trophy', 'trophy', 'trophy'], [link._icon_name for link in links])
        self.assertEqual(['/welcome', '/ranking', '/challenges'], [link._href for link in links])

    def test_intro_can_be_hidden_without_hiding_challenges_or_ranking(self):
        page = MagicMock()
        module = module_mira_challs()
        with patch.object(module_mira_challs, 'href', side_effect=lambda name: '/' + name), \
             patch.object(module, 'get_config_value', return_value=False), \
             patch('gdo.base.Application.Application.get_mode', return_value=None):
            module.gdo_init_sidebar(page)
        links = [call.args[0]._href for call in page._left_bar.add_field.call_args_list]
        self.assertEqual(['/ranking', '/challenges'], links)

    def test_default_depends_on_main_module(self):
        module = module_mira_challs()
        for main, expected in (('mira_challs', '1'), ('core', '0')):
            with self.subTest(main=main), \
                 patch('gdo.mira_challs.module_mira_challs.Application.config', return_value=main), \
                 patch('gdo.ui.WithIcon.t', side_effect=lambda key: key):
                fields = {field.get_name(): field for field in module.gdo_module_config()}
                self.assertEqual(expected, fields['show_intro_link'].get_initial())
