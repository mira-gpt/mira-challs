import hashlib
import unittest
from unittest.mock import MagicMock, patch

from gdo.mira_challs.challs.Errection.Errection import Errection, expected_answer


class ErrectionTest(unittest.TestCase):
    def test_answer_normalization_and_sha512(self):
        self.assertEqual(hashlib.sha512(b'hellowrld').hexdigest(),
                         expected_answer('Hello, Wörld! 123'))

    def test_install_and_verify(self):
        with patch('gdo.mira_challs.challs.Errection.Errection.secret_text', return_value='Hello world!'):
            values = Errection().install_values()
        self.assertEqual(2, values['chall_score'])
        record = MagicMock()
        record.gdo_val.return_value = values['chall_secret']
        with patch('gdo.mira_challs.GDO_Challenge.GDO_Challenge.table') as table:
            table.return_value.get_by_vals.return_value = record
            self.assertTrue(Errection().check_answer(expected_answer('Hello world!')))
            self.assertFalse(Errection().check_answer('0' * 128))
            self.assertFalse(Errection().check_answer('wrong'))

    def test_message_is_escaped_and_html_renders(self):
        method = MagicMock()
        method.t.side_effect = lambda key, args: '<pre>' + args[0] + '</pre>'
        with patch('gdo.mira_challs.challs.Errection.Errection.secret_text', return_value='<test>\nline'), \
             patch('gdo.mira_challs.challs.Errection.Errection.GDT_AnswerBox'):
            page = Errection.challenge_page(method)
        info = page.get_fields()[0].get_content().get_fields()[0].render_html()
        self.assertEqual('<pre>&lt;test&gt;\nline</pre>', info)
