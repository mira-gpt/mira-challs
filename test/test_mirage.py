import unittest
from unittest.mock import MagicMock, patch

from gdo.mira_challs.challs.Mirage.Mirage import Mirage


class MirageTest(unittest.TestCase):
    def test_install_and_case_insensitive_answer(self):
        with patch('gdo.mira_challs.challs.Mirage.Mirage.secret_answer', return_value='testanswer'):
            values = Mirage().install_values()
        record = MagicMock()
        record.gdo_val.return_value = values['chall_secret']
        with patch('gdo.mira_challs.GDO_Challenge.GDO_Challenge.table') as table:
            table.return_value.get_by_vals.return_value = record
            self.assertTrue(Mirage().check_answer('TESTAnswer'))
            self.assertFalse(Mirage().check_answer('wrong'))
            self.assertFalse(Mirage().check_answer('a' * 73))

    def test_page_html_escapes_name(self):
        method = MagicMock()
        method._env_user.get_name.return_value = '<guest>'
        method.t.side_effect = lambda key, args: '<p>' + args[0] + '</p>'
        with patch('gdo.mira_challs.challs.Mirage.Mirage.GDT_AnswerBox'):
            page = Mirage.challenge_page(method)
        info = page.get_fields()[0].get_content().get_fields()[0].render_html()
        self.assertEqual('<p>&lt;guest&gt;</p>', info)


if __name__ == '__main__':
    unittest.main()
