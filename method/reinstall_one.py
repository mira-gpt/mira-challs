from gdo.base.util.href import href
from gdo.core.GDT_String import GDT_String
from gdo.form.MethodForm import MethodForm
from gdo.mira_challs.ChallengeBoards import ChallengeBoards
from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.tags.GDT_Tags import GDT_Tags


class reinstall_one(MethodForm):
    """Reapply code-defined metadata to an installed challenge in place."""

    def gdo_connectors(self):
        return 'web'

    def gdo_user_permission(self):
        return 'owner'

    def gdo_parameters(self):
        return [GDT_String('named').not_null().positional()]

    def gdo_create_form(self, form):
        form.text('md_mira_challs_reinstall_one', (self.param_val('named'),))
        super().gdo_create_form(form)

    def form_submitted(self):
        name = self.param_val('named')
        destination = href('mira_challs', 'challenges')
        record = GDO_Challenge.table().get_by_vals({'chall_name': name})
        if not record:
            return self.redirect_err(destination, 'err_mira_challs_reinstall_unavailable', (name,))
        try:
            challenge = GDO_Challenge.load_challenge(name)
            values = challenge.install_values()
            tags = GDT_Tags.parse_names(challenge.get_challenge_tags())
        except (OSError, ValueError, ImportError, AttributeError, TypeError, NotImplementedError):
            return self.redirect_err(destination, 'err_mira_challs_reinstall_unavailable', (name,))
        record.save_vals(values)
        for tag in tags:
            record.add_tag(tag, allow_creation=True)
        ChallengeBoards.ensure([record])
        return self.redirect_msg(destination, 'msg_mira_challs_reinstalled', (name,))
