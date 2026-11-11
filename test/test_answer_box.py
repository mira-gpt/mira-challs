import unittest

from unittest.mock import patch

from gdo.base.Application import Application
from gdo.base.Render import Mode
from gdo.form.GDT_Form import GDT_Form
from gdo.mira_challs.GDT_AnswerBox import GDT_AnswerBox


class AnswerBoxTest(unittest.TestCase):
    def test_form_targets_solve_with_an_answer_and_submit(self):
        Application.mode(Mode.render_html)
        with patch('gdo.mira_challs.GDT_AnswerBox.href', return_value='/mira_challs.solve.named.BJ.html') as route, \
             patch('gdo.ui.WithIcon.t', side_effect=lambda key: key):
            form = GDT_AnswerBox(challenge_name='BJ')
        self.assertIsInstance(form, GDT_Form)
        route.assert_called_once_with('mira_challs', 'solve', 'named=BJ')
        self.assertEqual('/mira_challs.solve.named.BJ.html', form.render_href())
        self.assertEqual('answer', form._fields[0].get_name())
        self.assertEqual(1, len(form.actions()._fields))
