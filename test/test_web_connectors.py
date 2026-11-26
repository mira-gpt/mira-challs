import unittest

from gdo.base.Application import Application
from gdo.base.Render import Mode
from gdo.mira_challs.method.challenge import challenge
from gdo.mira_challs.method.challenges import challenges
from gdo.mira_challs.method.solve import solve


class ChallengeConnectorTest(unittest.TestCase):
    def test_requested_methods_are_web_only(self):
        Application.mode(Mode.render_cli)
        for method in (challenge, challenges, solve):
            with self.subTest(method=method.__name__):
                self.assertEqual('web', method().gdo_connectors())
