import unittest
from unittest.mock import MagicMock, patch

from gdo.base.Application import Application
from gdo.base.Render import Mode
from gdo.mira_challs.GDT_ChallSecret import GDT_ChallSecret
from gdo.mira_challs.method.solve import solve


class SolveTest(unittest.TestCase):
    def setUp(self):
        Application.mode(Mode.render_html)
        self.method = solve()
        self.challenge = MagicMock()
        self.record = MagicMock()
        self.record.get_id.return_value = '12'
        self.challenge.on_solved.return_value = True
        self.method._env_user = MagicMock()
        self.method._env_user.get_id.return_value = '34'
        self.form = MagicMock()
        self.form.get_field.return_value.get_val.return_value = 'answer'

    def submit(self):
        with patch.object(self.method, 'param_val', return_value='BJ'), \
             patch.object(self.method, 'get_form', return_value=self.form), \
             patch('gdo.mira_challs.method.solve.GDO_Challenge.load_challenge', return_value=self.challenge), \
             patch('gdo.mira_challs.method.solve.GDO_Challenge.table') as table, \
             patch.object(self.method, 'msg', side_effect=lambda key: key), \
             patch.object(self.method, 'err', side_effect=lambda key: key):
            table.return_value.get_by_vals.return_value = self.record
            result = self.method.form_submitted()
            if result == 'msg_mira_challs_answer_correct':
                self.challenge.on_solved.assert_called_once_with(self.method._env_user)
            return result

    def test_fixed_hash(self):
        self.record.gdo_val.return_value = GDT_ChallSecret.hash('answer')
        self.assertEqual('msg_mira_challs_answer_correct', self.submit())
        self.form.get_field.return_value.get_val.return_value = 'incorrect'
        self.assertEqual('err_mira_challs_wrong_answer', self.submit())
        self.challenge.check_answer.assert_not_called()

    def test_custom_checker(self):
        self.record.gdo_val.return_value = None
        self.challenge.check_answer.return_value = True
        self.assertEqual('msg_mira_challs_answer_correct', self.submit())
        self.challenge.check_answer.assert_called_once_with('answer')

    def test_missing_custom_checker(self):
        self.record.gdo_val.return_value = None
        self.challenge.check_answer.side_effect = NotImplementedError
        self.assertEqual('err_mira_challs_solve_unavailable', self.submit())

    def test_existing_solve_is_not_inserted_again(self):
        self.record.gdo_val.return_value = None
        self.challenge.check_answer.return_value = True
        self.challenge.on_solved.return_value = False
        self.assertEqual('msg_mira_challs_already_solved', self.submit())
