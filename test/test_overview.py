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
        created = MagicMock()
        created.copy_as.return_value.label.return_value = 'age'
        score = MagicMock()
        score.copy_as.return_value.shrink.return_value = 'score'
        table.columns.return_value = {'chall_name': 'name', 'chall_score': score,
                                      'chall_solvercount': 'solvers', 'chall_secret': 'secret',
                                      'chall_created': created, 'chall_last_solver': 'last solver',
                                      'chall_last_solved': 'last solved'}
        with patch('gdo.mira_challs.method.challenges.GDO_Challenge.table', return_value=table):
            self.assertIsInstance(self.method, MethodQueryTable)
            self.assertFalse(self.method.gdo_needs_authentication())
            self.assertEqual(self.method.gdo_table_headers(),
                             ['score', 'name', 'solvers', 'age', 'last solver', 'last solved'])
        created.copy_as.return_value.label.assert_called_once_with('chall_released')
        score.copy_as.return_value.shrink.assert_called_once_with()

    def test_release_shows_short_date_and_age(self):
        field = MagicMock()
        field.get_val.return_value = '2026-11-20 10:23:00'
        field.render_format.side_effect = ['11/20/2026 10:23', '2 days ago']
        self.assertEqual(self.method.render_chall_created(field, None),
                         '11/20/2026 10:23 (2 days ago)')
        self.assertEqual([call.args[0] for call in field.render_format.call_args_list], ['short', 'ago'])

    def test_release_missing_date(self):
        field = MagicMock()
        field.get_val.return_value = None
        self.assertEqual(self.method.render_chall_created(field, None), '---')

    def test_solver_count_is_derived_and_not_cached(self):
        table = MagicMock()
        query = table.select.return_value
        table.column.return_value.select_into.return_value = query
        query.nocache.return_value = query
        with patch.object(self.method, 'gdo_table', return_value=table), \
                patch.object(self.method, 'param_value', return_value=None):
            self.assertIs(query, self.method.gdo_table_query())
        self.assertEqual([call.args[0] for call in table.column.call_args_list],
                         ['chall_solvercount', 'chall_last_solver', 'chall_last_solved'])
        self.assertEqual(3, table.column.return_value.select_into.call_count)
        query.nocache.assert_called_once()

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
