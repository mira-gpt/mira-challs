import unittest
from pathlib import Path

from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.tags.GDT_Tags import GDT_Tags


class ChallengeTagsTest(unittest.TestCase):
    def test_default_and_each_challenge_override(self):
        self.assertEqual('challenge', GDO_Challenge().get_challenge_tags())
        challenges = Path(__file__).resolve().parents[1] / 'challs'
        names = sorted(path.name for path in challenges.iterdir()
                       if path.is_dir() and (path / f'{path.name}.py').is_file())
        self.assertTrue(names)
        for name in names:
            with self.subTest(challenge=name):
                challenge = GDO_Challenge.load_challenge(name)
                self.assertIn('get_challenge_tags', type(challenge).__dict__)
                self.assertIn('challenge', GDT_Tags.parse_names(challenge.get_challenge_tags()))
