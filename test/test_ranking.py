import unittest
from unittest.mock import MagicMock, patch

from gdo.mira_challs.method.ranking import ranking
from gdo.table.MethodQueryTable import MethodQueryTable


class RankingTest(unittest.TestCase):
    def setUp(self):
        with patch('gdo.base.Application.Application.get_mode', return_value=None):
            self.method = ranking()

    def test_public_ranking_uses_completed_solves_and_stable_order(self):
        table = MagicMock()
        query = table.select.return_value
        query.select.return_value = query.join.return_value = query.where.return_value = query.order.return_value = query.nocache.return_value = query
        with patch.object(self.method, 'gdo_table', return_value=table):
            self.assertIs(query, self.method.gdo_table_query())
        self.assertIsInstance(self.method, MethodQueryTable)
        self.assertFalse(self.method.gdo_needs_authentication())
        self.assertIn('s.solve_timestamp IS NOT NULL', query.where.call_args.args[0])
        query.order.assert_called_once_with('chall_points DESC, gdo_user.user_id ASC')
        query.nocache.assert_called_once()

    def test_render_rank_advances_from_current_page_offset(self):
        self.method._curr_table_row_id = 10
        self.assertEqual('11', self.method.render_rank(None, None))
        self.assertEqual('12', self.method.render_rank(None, None))

    def test_user_link_escapes_name_and_includes_server(self):
        user = MagicMock()
        user.get_id.return_value = '7'
        user.gdo_val.side_effect = lambda key: {'user_name': '<Ada>', 'ranking_server': 'Web'}[key]
        with patch('gdo.base.Application.Application.get_mode', return_value=None), \
             patch('gdo.mira_challs.method.ranking.href', return_value='/profile'):
            html = self.method.render_user_name(None, user)
        self.assertIn('&lt;Ada&gt;{web}', html)
        self.assertNotIn('<Ada>', html)
