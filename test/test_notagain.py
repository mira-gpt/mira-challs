import hashlib
import unittest
from unittest.mock import MagicMock, patch

from gdo.mira_challs.challs.NotAgain.NotAgain import NotAgain, compatible, expected_answer, MORSE


class NotAgainTest(unittest.TestCase):
    def test_info_renders_html(self):
        method = MagicMock()
        method.t.return_value = '<p>Message</p><code>...---</code>'
        with patch('gdo.mira_challs.challs.NotAgain.NotAgain.plaintext', return_value='SOS'), \
             patch('gdo.mira_challs.challs.NotAgain.NotAgain.GDT_AnswerBox'):
            page = NotAgain.challenge_page(method)
        card = page.get_fields()[0]
        info = card.get_content().get_fields()[0].render_html()
        self.assertEqual('<p>Message</p><code>...---</code>', info)

    def test_morse_and_solution(self):
        self.assertEqual('SOS 42!', compatible('sos 42!\n'))
        self.assertEqual('...---...', ''.join(MORSE.get(c, '') for c in compatible('SOS')))
        self.assertEqual(hashlib.sha512(b'SOS42!').hexdigest().upper(), expected_answer('sos 42!\n'))

    def test_install_and_check(self):
        with patch('gdo.mira_challs.challs.NotAgain.NotAgain.plaintext', return_value='SOS'):
            values = NotAgain().install_values()
        self.assertEqual('NotAgain', values['chall_name'])
        record = MagicMock()
        record.gdo_val.return_value = values['chall_secret']
        with patch('gdo.mira_challs.GDO_Challenge.GDO_Challenge.table') as table:
            table.return_value.get_by_vals.return_value = record
            self.assertTrue(NotAgain().check_answer(expected_answer('SOS')))
            self.assertFalse(NotAgain().check_answer('0' * 128))
            self.assertFalse(NotAgain().check_answer('short'))
