from importlib import invalidate_caches
from pathlib import Path
import re

from gdo.core.GDT_String import GDT_String
from gdo.form.MethodForm import MethodForm
from gdo.mira_challs.module_mira_challs import module_mira_challs
from gdo.mira_challs.GDO_Challenge import GDO_Challenge


def discover_challenges(directory=None):
    directory = Path(directory if directory is not None else module_mira_challs.instance().file_path('challs'))
    available, incomplete = [], []
    invalidate_caches()
    for folder in sorted(directory.iterdir()):
        name = folder.name
        if not folder.is_dir() or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', name):
            continue
        if GDO_Challenge.table().get_by_vals({'chall_name': name}):
            continue
        if not (folder / f'{name}.py').is_file():
            incomplete.append(name)
            continue
        try:
            GDO_Challenge.load_challenge(name)
        except (AttributeError, TypeError, ImportError, ValueError):
            incomplete.append(name)
            continue
        available.append(name)
    return available, incomplete


class install(MethodForm):
    def gdo_connectors(self) -> str:
        return 'web'

    def gdo_user_permission(self) -> str | None:
        return 'admin'

    def gdo_create_form(self, form):
        available, incomplete = discover_challenges()
        summary = self.t('msg_mira_challs_install_candidates', (', '.join(available) or '-',))
        if incomplete:
            summary += ' ' + self.t('msg_mira_challs_install_incomplete', (', '.join(incomplete),))
        form.text_raw(summary)
        form.add_field(GDT_String('candidates').maxlen(8192).hidden().initial(','.join(available)))
        super().gdo_create_form(form)

    def form_submitted(self):
        requested = set((self.get_form().get_field('candidates').get_val() or '').split(','))
        available, _ = discover_challenges()
        installed = []
        for name in available:
            if name in requested and not GDO_Challenge.table().get_by_vals({'chall_name': name}):
                GDO_Challenge.blank({'chall_name': name}).insert()
                installed.append(name)
        return self.msg('msg_mira_challs_installed', (', '.join(installed) or '-',))
