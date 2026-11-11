import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from gdo.mira_challs.method.install import discover_challenges, install


class InstallTest(unittest.TestCase):
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

    def test_only_previewed_candidates_are_installed(self):
        with patch('gdo.base.Application.Application.get_mode', return_value=None):
            method = install()
        form = MagicMock()
        form.get_field.return_value.get_val.return_value = 'BJ,Already'
        table = MagicMock()
        table.get_by_vals.side_effect = lambda vals: vals['chall_name'] == 'Already'
        record = MagicMock()
        with patch.object(method, 'get_form', return_value=form), \
             patch.object(method, 'msg', return_value='ok'), \
             patch('gdo.mira_challs.method.install.discover_challenges', return_value=(['BJ', 'Already', 'New'], [])), \
             patch('gdo.mira_challs.method.install.GDO_Challenge.table', return_value=table), \
             patch('gdo.mira_challs.method.install.GDO_Challenge.blank', return_value=record) as blank:
            self.assertEqual(method.form_submitted(), 'ok')
            blank.assert_called_once_with({'chall_name': 'BJ'})
            record.insert.assert_called_once()

    def test_form_displays_discovered_challenges(self):
        with patch('gdo.base.Application.Application.get_mode', return_value=None):
            method = install()
        form = MagicMock()
        with patch('gdo.mira_challs.method.install.discover_challenges', return_value=(['BJ', 'APPLY'], ['Mirage'])), \
             patch.object(method, 't', side_effect=lambda key, args: f'{key}: {args[0]}'), \
             patch('gdo.form.MethodForm.MethodForm.gdo_create_form'):
            method.gdo_create_form(form)
        form.text_raw.assert_called_once_with(
            'msg_mira_challs_install_candidates: BJ, APPLY msg_mira_challs_install_incomplete: Mirage')
