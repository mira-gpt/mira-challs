import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from gdo.mira_challs.method.install import discover_challenges, install
from gdo.mira_challs.method.install_one import install_one


class InstallTest(unittest.TestCase):
    def test_install_methods_require_owner(self):
        with patch('gdo.base.Application.Application.get_mode', return_value=None):
            self.assertEqual('owner', install().gdo_user_permission())
            self.assertEqual('owner', install_one().gdo_user_permission())

    def test_default_directory_uses_module_file_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            module = MagicMock()
            module.file_path.return_value = tmp
            with patch('gdo.mira_challs.method.install.module_mira_challs.instance', return_value=module):
                self.assertEqual(discover_challenges(), ([], []))
            module.file_path.assert_called_once_with('challs')

    def test_discovery_skips_installed_and_incomplete(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for name in ('BJ', 'Already', 'Incomplete', 'Broken'):
                (root / name).mkdir()
                if name != 'Incomplete':
                    (root / name / f'{name}.py').touch()
            table = MagicMock()
            table.get_by_vals.side_effect = lambda vals: vals['chall_name'] == 'Already'
            def load(name):
                if name == 'Broken':
                    raise AttributeError(name)
                return object()
            with patch('gdo.mira_challs.method.install.GDO_Challenge.table', return_value=table), \
                 patch('gdo.mira_challs.method.install.GDO_Challenge.load_challenge', side_effect=load):
                self.assertEqual(discover_challenges(root), (['BJ'], ['Broken', 'Incomplete']))

    def test_table_lists_ready_and_incomplete(self):
        from gdo.table.MethodTable import MethodTable
        with patch('gdo.base.Application.Application.get_mode', return_value=None):
            method = install()
        table = MagicMock()
        with patch('gdo.mira_challs.method.install.discover_challenges', return_value=(['BJ'], ['Mirage'])), \
             patch('gdo.mira_challs.method.install.GDO_Challenge.table', return_value=table), \
             patch('gdo.mira_challs.method.install.GDO_Challenge.blank', side_effect=lambda vals: vals['chall_name']):
            self.assertIsInstance(method, MethodTable)
            self.assertEqual(['BJ', 'Mirage'], method.gdo_table_result()._data)

    def test_each_ready_row_has_post_form_incomplete_has_none(self):
        with patch('gdo.base.Application.Application.get_mode', return_value=None):
            method = install()
        method._install_candidates = (['BJ', 'APPLY'], ['Mirage'])
        challenge = MagicMock()
        challenge.gdo_val.return_value = 'Mirage'
        self.assertEqual('', method.render_install_action(None, challenge))
        challenge.gdo_val.return_value = 'BJ'
        forms = []
        with patch('gdo.mira_challs.method.install.href', return_value='/install/BJ'), \
             patch('gdo.form.GDT_CSRF.GDT_CSRF.generate_token', return_value='test-token') as token, \
             patch('gdo.form.GDT_Form.GDT_Form.render_html', autospec=True, side_effect=lambda form: forms.append(form) or 'post form'):
            self.assertEqual('post form', method.render_install_action(None, challenge))
            challenge.gdo_val.return_value = 'APPLY'
            self.assertEqual('post form', method.render_install_action(None, challenge))
        token.assert_called_once()
        self.assertEqual(['test-token', 'test-token'], [form.get_field('csrf').get_val() for form in forms])
        self.assertTrue(all(form._http_method == 'POST' for form in forms))

    def test_only_requested_ready_challenge_is_installed(self):
        with patch('gdo.base.Application.Application.get_mode', return_value=None):
            method = install_one()
        method.param_val = MagicMock(return_value='BJ')
        method.redirect_msg = MagicMock(return_value='ok')
        table = MagicMock()
        table.get_by_vals.return_value = None
        record = MagicMock()
        with patch('gdo.mira_challs.method.install_one.href', return_value='/install'), \
             patch('gdo.mira_challs.method.install_one.discover_challenges', return_value=(['BJ', 'APPLY'], [])), \
             patch('gdo.mira_challs.method.install_one.GDO_Challenge.load_challenge') as load, \
             patch('gdo.mira_challs.method.install_one.GDO_Challenge.table', return_value=table), \
             patch('gdo.mira_challs.method.install_one.GDO_Challenge.blank', return_value=record) as blank:
            load.return_value.install_values.return_value = {'chall_name': 'BJ'}
            self.assertEqual(method.form_submitted(), 'ok')
            blank.assert_called_once_with({'chall_name': 'BJ'})
            record.insert.assert_called_once()

    def test_incomplete_or_already_installed_is_not_inserted(self):
        with patch('gdo.base.Application.Application.get_mode', return_value=None):
            method = install_one()
        method.param_val = MagicMock(return_value='Mirage')
        method.redirect_err = MagicMock(return_value='unavailable')
        with patch('gdo.mira_challs.method.install_one.href', return_value='/install'), \
             patch('gdo.mira_challs.method.install_one.discover_challenges', return_value=(['BJ'], ['Mirage'])), \
             patch('gdo.mira_challs.method.install_one.GDO_Challenge.blank') as blank:
            self.assertEqual('unavailable', method.form_submitted())
            blank.assert_not_called()

    def test_concurrent_install_is_not_overwritten(self):
        with patch('gdo.base.Application.Application.get_mode', return_value=None):
            method = install_one()
        method.param_val = MagicMock(return_value='BJ')
        method.redirect_err = MagicMock(return_value='unavailable')
        table = MagicMock()
        table.get_by_vals.return_value = MagicMock()
        with patch('gdo.mira_challs.method.install_one.href', return_value='/install'), \
             patch('gdo.mira_challs.method.install_one.discover_challenges', return_value=(['BJ'], [])), \
             patch('gdo.mira_challs.method.install_one.GDO_Challenge.table', return_value=table), \
             patch('gdo.mira_challs.method.install_one.GDO_Challenge.blank') as blank:
            self.assertEqual('unavailable', method.form_submitted())
            blank.assert_not_called()
