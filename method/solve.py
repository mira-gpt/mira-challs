from gdo.base.GDT import GDT
from gdo.core.GDT_String import GDT_String
from gdo.form.MethodForm import MethodForm
from gdo.mira_challs.GDO_Challenge import GDO_Challenge


class solve(MethodForm):
    def gdo_parameters(self) -> list[GDT]:
        return [
            GDT_String('named').not_null().positional(),
        ]

    def gdo_create_form(self, form):
        form.add_field(GDT_String('answer').maxlen(512).label('mira_challs_answer').not_null())
        super().gdo_create_form(form)

    def form_submitted(self):
        name = self.param_val('named')
        challenge = GDO_Challenge.load_challenge(name)
        record = GDO_Challenge.table().get_by_vals({'chall_name': name})
        if not record:
            return self.err('err_mira_challs_solve_unavailable')
        answer = self.get_form().get_field('answer').get_val()
        try:
            valid = challenge.check_answer_for_user(answer, self._env_user)
        except (NotImplementedError, ValueError, OSError):
            return self.err('err_mira_challs_solve_unavailable')
        if not valid:
            return self.err('err_mira_challs_wrong_answer')
        result = challenge.on_solved(self._env_user)
        if result is None:
            return self.err('err_mira_challs_solve_unavailable')
        if not result:
            return self.msg('msg_mira_challs_already_solved')
        return self.msg('msg_mira_challs_answer_correct')
