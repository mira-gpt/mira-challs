from gdo.base.util.href import href
from gdo.core.GDT_String import GDT_String
from gdo.form.MethodForm import MethodForm
from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.mira_challs.method.install import discover_challenges


class install_one(MethodForm):
    def gdo_connectors(self):
        return 'web'

    def gdo_user_permission(self):
        return 'owner'

    def gdo_parameters(self):
        return [GDT_String('named').not_null().positional()]

    def gdo_create_form(self, form):
        form.text('md_mira_challs_install_one', (self.param_val('named'),))
        super().gdo_create_form(form)

    def form_submitted(self):
        name = self.param_val('named')
        ready, _ = discover_challenges()
        destination = href('mira_challs', 'install')
        if name not in ready or GDO_Challenge.table().get_by_vals({'chall_name': name}):
            return self.redirect_err(destination, 'err_mira_challs_install_unavailable', (name,))
        try:
            values = GDO_Challenge.load_challenge(name).install_values()
        except (OSError, ValueError):
            return self.redirect_err(destination, 'err_mira_challs_install_unavailable', (name,))
        GDO_Challenge.blank(values).insert()
        return self.redirect_msg(destination, 'msg_mira_challs_installed', (name,))
