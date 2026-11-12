import unittest
from unittest.mock import MagicMock, patch

from gdo.core.GDT_String import GDT_String
from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.base.Application import Application
from gdo.base.Render import Mode


class ChallengeDescriptionTest(unittest.TestCase):
    def setUp(self):
        Application.mode(Mode.render_html)

    def test_description_stores_a_language_key(self):
        with patch('gdo.core.GDO_User.GDO_User.table', return_value=MagicMock()):
            description = next(field for field in GDO_Challenge().gdo_columns()
                               if field.get_name() == 'chall_description')
        self.assertIsInstance(description, GDT_String)
        description.val('mc_beiruth_description')
        self.assertEqual('mc_beiruth_description', description.get_val())

    def test_info_is_plain_and_omits_placeholders(self):
        from gdo.mira_challs.challs.Supreme.Supreme import Supreme
        with patch('gdo.mira_challs.GDO_Challenge.thas', return_value=True), \
             patch('gdo.mira_challs.GDO_Challenge.t', return_value='<p>Hello %s,</p><p>Find <a href="%s">clues</a> &amp; solve.</p>'):
            self.assertEqual('Hello, Find clues & solve.', Supreme().get_challenge_info())

    def test_metadata_contains_escaped_title_and_excerpt(self):
        from gdo.mira_challs.method.challenge import challenge
        method = challenge()
        method.param_val = MagicMock(return_value='Supreme')
        obj = MagicMock()
        obj.get_challenge_info.return_value = 'A "clue" & ' + 'x' * 200
        with patch.object(GDO_Challenge, 'load_challenge', return_value=obj), \
             patch('gdo.mira_challs.method.challenge.thas', return_value=True), \
             patch('gdo.mira_challs.method.challenge.t', side_effect=lambda key, args=None: 'Supreme' if args is None else '%s: %s' % args):
            description = method.gdo_render_descr()
        self.assertTrue(description.startswith('Supreme: A &quot;clue&quot; &amp;'))
        self.assertEqual(160, len(obj.get_challenge_info.return_value[:160]))
        self.assertNotIn('<', description)

    def test_invalid_challenge_has_safe_fallback(self):
        from gdo.mira_challs.method.challenge import challenge
        method = challenge()
        method.param_val = MagicMock(return_value='../invalid')
        with patch('gdo.mira_challs.method.challenge.t', return_value='Explore challenges.'):
            self.assertEqual('Explore challenges.', method.gdo_render_descr())
