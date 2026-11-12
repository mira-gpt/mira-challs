from gdo.core.GDT_User import GDT_User
from gdo.form.MethodForm import MethodForm
from gdo.mira_challs.challs.APPLY.APPLY import APPLY


class apply_approve(MethodForm):
    """Record an administrator's review of an APPLY submission."""

    def gdo_connectors(self):
        return 'web'

    def gdo_user_permission(self):
        return 'admin'

    def gdo_create_form(self, form):
        form.text('md_mira_challs_apply_approve')
        form.add_field(GDT_User('user').not_null().with_completion())
        super().gdo_create_form(form)

    def form_submitted(self):
        user = self.param_value('user')
        result = APPLY().on_solved(user)
        if result is None:
            return self.err('err_mira_challs_apply_unavailable')
        if not result:
            return self.msg('msg_mira_challs_apply_already_solved')
        return self.msg('msg_mira_challs_apply_approved')
