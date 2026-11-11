import unittest

from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.mira_challs.challs.APPLY.APPLY import APPLY
from gdo.mira_challs.challs.BJ.BJ import BJ


class LoadChallengeTest(unittest.TestCase):
    def test_loads_named_challenge_instances(self):
        loader = GDO_Challenge()
        self.assertIsInstance(loader.load_challenge('BJ'), BJ)
        self.assertIsInstance(loader.load_challenge('APPLY'), APPLY)

    def test_rejects_invalid_and_unknown_names(self):
        loader = GDO_Challenge()
        for name in ('../BJ', 'BJ.BJ', '', None):
            with self.subTest(name=name), self.assertRaises(ValueError):
                loader.load_challenge(name)
        with self.assertRaises(ModuleNotFoundError):
            loader.load_challenge('Missing')
