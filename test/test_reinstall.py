import unittest
from unittest.mock import MagicMock, patch

from gdo.base.Application import Application
from gdo.form.GDT_Form import GDT_Form
from gdo.mira_challs.method.reinstall_one import reinstall_one


class ReinstallTest(unittest.TestCase):
    def method(self):
        with patch.object(Application, 'get_mode', return_value=None):
            method = reinstall_one()
        method.param_val = MagicMock(return_value='BJ')
        method.redirect_msg = MagicMock(return_value='ok')
        method.redirect_err = MagicMock(return_value='error')
        return method

    def test_owner_and_confirmation(self):
        method = self.method()
        self.assertEqual('owner', method.gdo_user_permission())
        form = GDT_Form()
        with patch.object(Application, 'IS_HTTP', True), \
             patch.object(Application, 'get_mode', return_value=None):
            method.gdo_create_form(form)
        self.assertEqual('POST', form._http_method)
        self.assertIsNotNone(form.get_field('csrf'))

    def test_reinstall_updates_same_record_and_ensures_board(self):
        method = self.method()
        record = MagicMock()
        table = MagicMock()
        table.get_by_vals.return_value = record
        with patch('gdo.mira_challs.method.reinstall_one.href', return_value='/challenges'), \
             patch.object(Application, 'get_mode', return_value=None), \
             patch('gdo.mira_challs.method.reinstall_one.GDO_Challenge.table', return_value=table), \
             patch('gdo.mira_challs.method.reinstall_one.GDO_Challenge.load_challenge') as load, \
             patch('gdo.mira_challs.method.reinstall_one.GDO_Challenge.blank') as blank, \
             patch('gdo.mira_challs.method.reinstall_one.ChallengeBoards.ensure') as ensure:
            load.return_value.install_values.return_value = {'chall_name': 'BJ', 'chall_score': 3}
            load.return_value.get_challenge_tags.return_value = 'math,fun'
            self.assertEqual('ok', method.form_submitted())
            record.save_vals.assert_called_once_with({'chall_name': 'BJ', 'chall_score': 3})
            self.assertEqual(2, record.add_tag.call_count)
            ensure.assert_called_once_with([record])
            blank.assert_not_called()
            record.delete.assert_not_called()

    def test_missing_challenge_does_not_create_or_modify(self):
        method = self.method()
        table = MagicMock()
        table.get_by_vals.return_value = None
        with patch('gdo.mira_challs.method.reinstall_one.href', return_value='/challenges'), \
             patch('gdo.mira_challs.method.reinstall_one.GDO_Challenge.table', return_value=table), \
             patch('gdo.mira_challs.method.reinstall_one.GDO_Challenge.load_challenge') as load:
            self.assertEqual('error', method.form_submitted())
            load.assert_not_called()
