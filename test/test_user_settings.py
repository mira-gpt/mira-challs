import unittest
from unittest.mock import MagicMock, patch

from gdo.country.GDT_Country import GDT_Country
from gdo.mira_challs.module_mira_challs import module_mira_challs


class TestUserSettings(unittest.TestCase):
    def test_scoring_country_setting(self):
        module = module_mira_challs()
        with patch('gdo.country.GDT_Country.GDO_Country.table', return_value=MagicMock()), \
                patch('gdo.ui.WithIcon.t', return_value='Country'):
            settings = module.gdo_user_settings()
        self.assertIn('country', module.gdo_dependencies())
        self.assertEqual(1, len(settings))
        self.assertIsInstance(settings[0], GDT_Country)
        self.assertEqual('country_of_scoring', settings[0].get_name())
