import unittest
from unittest.mock import patch

from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.mira_challs.challs.APPLY.APPLY import APPLY
from gdo.mira_challs.challs.BJ.BJ import BJ
from gdo.mira_challs.challs.Errection.Errection import Errection
from gdo.mira_challs.challs.Mirage.Mirage import Mirage
from gdo.mira_challs.challs.NotAgain.NotAgain import NotAgain


class ChallengeScoreTest(unittest.TestCase):
    def test_scores_are_in_install_values(self):
        with patch('gdo.mira_challs.challs.Errection.Errection.secret_text', return_value='test'), \
             patch('gdo.mira_challs.challs.Mirage.Mirage.secret_answer', return_value='test'), \
             patch('gdo.mira_challs.challs.NotAgain.NotAgain.plaintext', return_value='test'):
            for challenge, score in ((APPLY(), 1), (BJ(), 3), (Errection(), 2),
                                     (Mirage(), 4), (NotAgain(), 8)):
                with self.subTest(challenge=type(challenge).__name__):
                    self.assertEqual(score, challenge.install_values()['chall_score'])

    def test_invalid_score_is_rejected(self):
        class Invalid(GDO_Challenge):
            _score = 11
        with self.assertRaises(ValueError):
            Invalid().install_values()
