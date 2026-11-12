import unittest
from unittest.mock import MagicMock, patch

from gdo.core.GDT_String import GDT_String
from gdo.mira_challs.GDO_Challenge import GDO_Challenge


class ChallengeDescriptionTest(unittest.TestCase):
    def test_description_stores_a_language_key(self):
        with patch('gdo.core.GDO_User.GDO_User.table', return_value=MagicMock()):
            description = next(field for field in GDO_Challenge().gdo_columns()
                               if field.get_name() == 'chall_description')
        self.assertIsInstance(description, GDT_String)
        description.val('mc_beiruth_description')
        self.assertEqual('mc_beiruth_description', description.get_val())
