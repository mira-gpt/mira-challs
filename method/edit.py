from gdo.base.util.href import href
from gdo.core.GDT_String import GDT_String
from gdo.form.MethodForm import MethodForm
from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.mira_challs.GDT_ChallSecret import GDT_ChallSecret
from gdo.tags.GDT_Tags import GDT_Tags
from gdo.ui.GDT_Score import GDT_Score


class StaticSolutionInput(GDT_String):
    def __init__(self, name):
        super().__init__(name)
        self._input_type = 'password'
        self.secret().maxlen(72)


def supports_static_answer(name):
    challenge = GDO_Challenge.load_challenge(name)
    return (type(challenge).check_answer is GDO_Challenge.check_answer and
            type(challenge).check_answer_for_user is GDO_Challenge.check_answer_for_user)


class edit(MethodForm):
    """Edit installed challenge metadata without changing its code identity."""

    def gdo_connectors(self):
        return 'web'

    def gdo_user_permission(self):
        return 'owner'

    def gdo_parameters(self):
        return [GDT_String('named').not_null().positional()]

    def get_challenge(self):
        return GDO_Challenge.table().get_by_vals({'chall_name': self.param_val('named')})

    def gdo_create_form(self, form):
        record = self.get_challenge()
        if record:
            tags = ', '.join(tag.gdo_val('tag_name') for tag in record.get_tags())
            form.add_fields(
                GDT_String('description').maxlen(128).initial(record.gdo_val('chall_description') or '').label('chall_description'),
                GDT_Score('score').min(1).max(10).not_null().initial(record.gdo_val('chall_score')).label('chall_score'),
                GDT_Tags('tags').maxlen(1024).initial(tags).label('mira_challs_edit_tags'),
            )
            if supports_static_answer(record.gdo_val('chall_name')):
                form.add_field(StaticSolutionInput('solution').label('mira_challs_edit_solution'))
            super().gdo_create_form(form)

    def gdo_execute(self):
        if not self.get_challenge():
            return self.err('err_mira_challs_edit_missing')
        return super().gdo_execute()

    def form_submitted(self):
        record = self.get_challenge()
        if not record:
            return self.err('err_mira_challs_edit_missing')
        form = self.get_form()
        try:
            names = GDT_Tags.parse_names(form.get_field('tags').get_val())
        except ValueError:
            return self.err('err_mira_challs_edit_tags')
        solution = None
        if supports_static_answer(record.gdo_val('chall_name')):
            solution = form.get_field('solution').get_val()
            if solution and len(solution.encode('utf-8')) > 72:
                return self.err('err_mira_challs_edit_solution')
        existing = {tag.gdo_val('tag_name').casefold(): tag.gdo_val('tag_name') for tag in record.get_tags()}
        desired = {name.casefold(): name for name in names}
        values = {'chall_description': form.get_field('description').get_val(),
                  'chall_score': form.get_field('score').get_val()}
        if solution:
            values['chall_secret'] = GDT_ChallSecret.hash(solution)
        record.save_vals(values)
        for key in existing.keys() - desired.keys():
            record.remove_tag(existing[key])
        for key in desired.keys() - existing.keys():
            record.add_tag(desired[key], allow_creation=True)
        return self.redirect_msg(href('mira_challs', 'challenges'), 'msg_mira_challs_edited')
