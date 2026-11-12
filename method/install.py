from importlib import invalidate_caches
from pathlib import Path
import re

from gdo.base.ResultArray import ResultArray
from gdo.base.util.href import href
from gdo.core.GDT_String import GDT_String
from gdo.form.GDT_CSRF import GDT_CSRF
from gdo.form.GDT_Form import GDT_Form
from gdo.form.GDT_Hidden import GDT_Hidden
from gdo.form.GDT_Submit import GDT_Submit
from gdo.mira_challs.module_mira_challs import module_mira_challs
from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.table.MethodTable import MethodTable


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


class install(MethodTable):
    def gdo_connectors(self) -> str:
        return 'web'

    def gdo_user_permission(self) -> str | None:
        return 'admin'

    def gdo_table(self):
        return GDO_Challenge.table()

    def gdo_table_headers(self):
        return [GDT_String('chall_name').label('chall_name'),
                GDT_String('install_status').label('mira_challs_install_status'),
                GDT_String('install_action').label('mira_challs_install_action')]

    def gdo_paginated(self):
        return False

    def gdo_ordered(self):
        return False

    def gdo_filtered(self):
        return False

    def gdo_searched(self):
        return False

    def candidates(self):
        if not hasattr(self, '_install_candidates'):
            self._install_candidates = discover_challenges()
        return self._install_candidates

    def gdo_table_result(self):
        ready, incomplete = self.candidates()
        rows = [GDO_Challenge.blank({'chall_name': name}) for name in sorted(ready + incomplete)]
        return ResultArray(rows, self.gdo_table())

    def render_install_status(self, field, challenge):
        key = 'mira_challs_ready' if challenge.gdo_val('chall_name') in self.candidates()[0] else 'mira_challs_incomplete'
        return self.t(key, ())

    def csrf_token(self):
        # One token per page, shared by the separate row forms. Generating one
        # per row would invalidate early rows when more than 17 are displayed.
        if not hasattr(self, '_install_csrf_token'):
            self._install_csrf_token = GDT_CSRF().generate_token()
        return self._install_csrf_token

    def render_install_action(self, field, challenge):
        name = challenge.gdo_val('chall_name')
        if name not in self.candidates()[0]:
            return ''
        form = GDT_Form().href(href('mira_challs', 'install_one', positional=(name,)))
        form.add_field(GDT_Hidden('csrf').val(self.csrf_token()))
        form.actions().add_field(GDT_Submit().text('mira_challs_install_button'))
        return form.render_html()
