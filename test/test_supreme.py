import unittest
from unittest.mock import MagicMock, patch

from gdo.mira_challs.challs.Supreme.Supreme import Supreme


class SupremeTest(unittest.TestCase):
    def test_install_and_case_sensitive_answer(self):
        with patch('gdo.mira_challs.challs.Supreme.Supreme.secret_answer', return_value='ExampleAnswer'):
            values = Supreme().install_values()
        self.assertEqual(3, values['chall_score'])
        record = MagicMock()
        record.gdo_val.return_value = values['chall_secret']
        with patch('gdo.mira_challs.GDO_Challenge.GDO_Challenge.table') as table:
            table.return_value.get_by_vals.return_value = record
            self.assertTrue(Supreme().check_answer('ExampleAnswer'))
            self.assertFalse(Supreme().check_answer('exampleanswer'))
            self.assertFalse(Supreme().check_answer('wrong'))
            self.assertFalse(Supreme().check_answer('x' * 73))

    def test_page_escapes_username_and_has_profile(self):
        method = MagicMock()
        method._env_user.get_name.return_value = '<guest>'
        method.t.side_effect = lambda key, args: f'<p>{args[0]} {args[1]}</p>'
        with patch('gdo.mira_challs.challs.Supreme.Supreme.GDT_AnswerBox'):
            page = Supreme.challenge_page(method)
        html = page.get_fields()[0].get_content().get_fields()[0].render_html()
        self.assertIn('&lt;guest&gt;', html)
        self.assertIn('https://backend.www.linkuup.de/user.profile.for.shqiprim.html', html)

    def test_missing_secret_fails_closed(self):
        with patch('gdo.mira_challs.challs.Supreme.Supreme.secret_answer', side_effect=FileNotFoundError):
            with self.assertRaises(FileNotFoundError):
                Supreme().install_values()
