import unittest
from unittest.mock import MagicMock, patch

from gdo.base.Application import Application
from gdo.base.Render import Mode
from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.mira_challs.method.edit import edit, supports_static_answer
from gdo.form.GDT_Form import GDT_Form


class StaticChallenge(GDO_Challenge):
    pass


class CustomChallenge(GDO_Challenge):
    def check_answer(self, answer):
        return False


class EditTest(unittest.TestCase):
    def setUp(self):
        Application.mode(Mode.render_html)
        self.method = edit()
        self.record = MagicMock()
        self.record.gdo_val.return_value = 'Static'
        tag = MagicMock()
        tag.gdo_val.return_value = 'old'
        self.record.get_tags.return_value = [tag]
        self.form = MagicMock()

    def fields(self, solution='', tags='new'):
        values = {'description': 'Updated', 'score': '5', 'tags': tags, 'solution': solution}
        self.form.get_field.side_effect = lambda key: MagicMock(get_val=MagicMock(return_value=values[key]))

    def test_requires_owner(self):
        self.assertEqual('owner', self.method.gdo_user_permission())
        self.assertEqual('web', self.method.gdo_connectors())

    def test_web_form_has_csrf_and_blank_static_solution(self):
        self.record.gdo_val.side_effect = lambda key: {
            'chall_name': 'Static', 'chall_description': 'Description', 'chall_score': '5'
        }[key]
        form = GDT_Form()
        with patch.object(Application, 'IS_HTTP', True), \
             patch.object(edit, 'get_challenge', return_value=self.record), \
             patch('gdo.mira_challs.method.edit.supports_static_answer', return_value=True):
            self.method.gdo_create_form(form)
        self.assertIsNotNone(form.get_field('csrf'))
        self.assertFalse(form.get_field('solution').get_val())
        self.assertTrue(form.get_field('solution').is_secret())

    def test_long_multibyte_solution_is_rejected_before_writes(self):
        self.fields(solution='é' * 37)
        with patch.object(edit, 'get_challenge', return_value=self.record), \
             patch.object(edit, 'get_form', return_value=self.form), \
             patch('gdo.mira_challs.method.edit.supports_static_answer', return_value=True), \
             patch.object(edit, 'err') as error:
            self.method.form_submitted()
        error.assert_called_once_with('err_mira_challs_edit_solution')
        self.record.save_vals.assert_not_called()

    def test_static_detection_rejects_custom_checker(self):
        with patch.object(GDO_Challenge, 'load_challenge', side_effect=[StaticChallenge(), CustomChallenge()]):
            self.assertTrue(supports_static_answer('Static'))
            self.assertFalse(supports_static_answer('Custom'))

    def test_blank_solution_preserves_hash_and_updates_tags(self):
        self.fields()
        with patch.object(edit, 'get_challenge', return_value=self.record), \
             patch.object(edit, 'get_form', return_value=self.form), \
             patch('gdo.mira_challs.method.edit.supports_static_answer', return_value=True), \
             patch('gdo.mira_challs.method.edit.href', return_value='/challenges'), \
             patch.object(edit, 'redirect_msg'):
            self.method.form_submitted()
        self.record.save_vals.assert_called_once_with({'chall_description': 'Updated', 'chall_score': '5'})
        self.record.remove_tag.assert_called_once_with('old')
        self.record.add_tag.assert_called_once_with('new', allow_creation=True)

    def test_static_solution_is_hashed(self):
        self.fields(solution='a new solution', tags='old')
        with patch.object(edit, 'get_challenge', return_value=self.record), \
             patch.object(edit, 'get_form', return_value=self.form), \
             patch('gdo.mira_challs.method.edit.supports_static_answer', return_value=True), \
             patch('gdo.mira_challs.method.edit.GDT_ChallSecret.hash', return_value='hash') as hasher, \
             patch('gdo.mira_challs.method.edit.href', return_value='/challenges'), \
             patch.object(edit, 'redirect_msg'):
            self.method.form_submitted()
        hasher.assert_called_once_with('a new solution')
        self.assertEqual('hash', self.record.save_vals.call_args.args[0]['chall_secret'])

    def test_invalid_tags_do_not_write(self):
        self.fields(tags='bad tag')
        with patch.object(edit, 'get_challenge', return_value=self.record), \
             patch.object(edit, 'get_form', return_value=self.form), \
             patch.object(edit, 'err'):
            self.method.form_submitted()
        self.record.save_vals.assert_not_called()
        self.record.add_tag.assert_not_called()

    def test_custom_checker_never_reads_solution(self):
        self.fields(tags='old')
        with patch.object(edit, 'get_challenge', return_value=self.record), \
             patch.object(edit, 'get_form', return_value=self.form), \
             patch('gdo.mira_challs.method.edit.supports_static_answer', return_value=False), \
             patch('gdo.mira_challs.method.edit.href', return_value='/challenges'), \
             patch.object(edit, 'redirect_msg'):
            self.method.form_submitted()
        self.assertNotIn('chall_secret', self.record.save_vals.call_args.args[0])
        self.assertNotIn('solution', [call.args[0] for call in self.form.get_field.call_args_list])
