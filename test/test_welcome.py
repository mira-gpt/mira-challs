import unittest
from unittest.mock import patch

from gdo.base.Application import Application
from gdo.base.Render import Mode
from gdo.mira_challs.method.welcome import welcome


class WelcomeTest(unittest.TestCase):
    def test_welcome_links_to_challenges(self):
        Application.mode(Mode.render_html)
        method = welcome()
        with patch('gdo.mira_challs.method.welcome.href', return_value='/challenges') as link, \
             patch.object(welcome, 't', return_value='<p>Welcome. <a href="/challenges">challenges</a></p>') as translate:
            method.gdo_execute()
        link.assert_called_once_with('mira_challs', 'challenges')
        translate.assert_called_once_with('msg_mira_challs_welcome', ('/challenges',))
