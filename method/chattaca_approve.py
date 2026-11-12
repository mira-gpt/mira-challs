from gdo.base.Method import Method
from gdo.core.GDT_User import GDT_User
from gdo.mira_challs.challs.ChATTACA.ChATTACA import ChATTACA


class chattaca_approve(Method):
    """Record a completed ChATTACA conversation via authenticated local Dog."""

    @classmethod
    def gdo_trigger(cls):
        return 'mira_challs.chattaca_approve'

    def gdo_connectors(self):
        return 'tcp'

    def gdo_user_permission(self):
        return 'owner'

    def gdo_needs_authentication(self):
        return True

    def gdo_parameters(self):
        return [GDT_User('user').not_null().positional()]

    def gdo_execute(self):
        user = self.param_value('user')
        result = ChATTACA().on_solved(user)
        if result is None:
            return self.err('err_mira_challs_chattaca_unavailable')
        if not result:
            return self.msg('msg_mira_challs_chattaca_already', (user.render_name(),))
        return self.msg('msg_mira_challs_chattaca_approved', (user.render_name(),))
