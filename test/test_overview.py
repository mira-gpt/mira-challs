import unittest
from unittest.mock import MagicMock, patch

from gdo.mira_challs.method.challenges import challenges
from gdo.table.MethodQueryTable import MethodQueryTable


class OverviewTest(unittest.TestCase):
    def setUp(self):
        with patch('gdo.base.Application.Application.get_mode', return_value=None):
            self.method = challenges()

    def test_public_query_table_exposes_only_public_columns(self):
        table = MagicMock()
        table.columns.return_value = {'chall_name': 'name', 'chall_score': 'score', 'chall_secret': 'secret'}
        with patch('gdo.mira_challs.method.challenges.GDO_Challenge.table', return_value=table):
            self.assertIsInstance(self.method, MethodQueryTable)
            self.assertFalse(self.method.gdo_needs_authentication())
            self.assertEqual(self.method.gdo_table_headers(), ['name', 'score'])

    def test_challenge_name_links_to_named_route(self):
        challenge = MagicMock()
        challenge.gdo_val.return_value = 'BJ'
        link = MagicMock()
        link.href.return_value = link.text_raw.return_value = link.icon.return_value = link
        link.render_html.return_value = 'link'
        with patch('gdo.mira_challs.method.challenges.href', return_value='/challenge') as make_href, \
             patch('gdo.mira_challs.method.challenges.GDT_Link', return_value=link):
            self.assertEqual(self.method.render_chall_name(None, challenge), 'link')
            make_href.assert_called_once_with('mira_challs', 'challenge', positional=('BJ',))
            link.text_raw.assert_called_once_with('BJ')
