import unittest
from unittest.mock import patch
from gdo.core.ChallengeToken import issue
from gdo.mira_challs.challs.BJ.BJ import BJ


class BJChallengeTest(unittest.TestCase):
    def test_valid_and_invalid_tokens(self):
        key = b'k' * 32
        token = issue(key, 'bj1', 'Blackjack player')
        with patch('gdo.mira_challs.challs.BJ.BJ.read_secret', return_value=key):
            self.assertTrue(BJ().check_answer(token))
            self.assertFalse(BJ().check_answer(token + 'x'))
            self.assertFalse(BJ().check_answer('not a token'))

    def test_missing_secret_is_not_treated_as_a_wrong_answer(self):
        with patch('gdo.mira_challs.challs.BJ.BJ.read_secret', side_effect=FileNotFoundError):
            with self.assertRaises(FileNotFoundError):
                BJ().check_answer('anything')
