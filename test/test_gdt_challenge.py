import unittest
from unittest.mock import patch, sentinel

from gdo.core.GDT_Object import GDT_Object
from gdo.mira_challs.GDT_Challenge import GDT_Challenge
from gdo.mira_challs.GDO_Challenge import GDO_Challenge


class ChallengeFieldTest(unittest.TestCase):
    def test_references_challenge_table(self):
        with patch('gdo.ui.WithIcon.t', side_effect=lambda key: key), \
             patch.object(GDO_Challenge, 'table', return_value=sentinel.table):
            field = GDT_Challenge('named')
        self.assertIsInstance(field, GDT_Object)
        self.assertIs(field._table, sentinel.table)
