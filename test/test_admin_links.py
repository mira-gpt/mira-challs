import unittest
from unittest.mock import patch

from gdo.mira_challs.module_mira_challs import module_mira_challs


class AdminLinksTest(unittest.TestCase):
    def test_install_link_uses_module_route_and_translation(self):
        module = module_mira_challs()
        with patch('gdo.base.Application.Application.get_mode', return_value=None), \
             patch.object(module, 'href', return_value='/mira_challs.install.html') as href:
            links = module.gdo_admin_links()
        href.assert_called_once_with('install')
        self.assertEqual(1, len(links))
        self.assertEqual('/mira_challs.install.html', links[0]._href)
        self.assertEqual('mt_mira_challs_install', links[0]._text_key)
