import unittest
from unittest.mock import MagicMock, patch

from gdo.mira_challs.challs.BJ.BJ import BJ


class ProgressTest(unittest.TestCase):
    def setUp(self):
        self.challenge = BJ()
        self.user = MagicMock()
        self.user.is_member.return_value = True
        self.user.get_id.return_value = '34'
        self.record = MagicMock()
        self.record.get_id.return_value = '12'

    def test_first_open_creates_start_and_repeat_preserves_it(self):
        with patch('gdo.mira_challs.GDO_Challenge.GDO_Challenge.table') as challenges, \
             patch('gdo.mira_challs.GDO_ChallengeSolved.GDO_ChallengeSolved.table') as solves, \
             patch('gdo.mira_challs.GDO_ChallengeSolved.GDO_ChallengeSolved.blank') as blank:
            challenges.return_value.get_by_vals.return_value = self.record
            solves.return_value.get_by_vals.return_value = None
            self.challenge.start(self.user)
            blank.assert_called_once_with({'solve_challenge': '12', 'solve_user': '34'})
            entry = MagicMock()
            solves.return_value.get_by_vals.return_value = entry
            self.assertIs(entry, self.challenge.start(self.user))
            blank.assert_called_once()

    def test_guest_does_not_create_start(self):
        self.user.is_member.return_value = False
        self.assertIsNone(self.challenge.start(self.user))

    def test_solved_sets_timestamp_only_once(self):
        entry = MagicMock()
        entry.gdo_val.return_value = None
        with patch.object(self.challenge, 'start', return_value=entry), \
             patch('gdo.mira_challs.GDO_Challenge.Time.get_date', return_value='2026-11-11 20:00:00'):
            self.assertTrue(self.challenge.on_solved(self.user))
            entry.save_val.assert_called_once_with('solve_timestamp', '2026-11-11 20:00:00')
            entry.gdo_val.return_value = '2026-11-11 20:00:00'
            self.assertFalse(self.challenge.on_solved(self.user))
            entry.save_val.assert_called_once()
