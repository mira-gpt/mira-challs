from gdo.base.Application import Application
from gdo.base.util.href import href
from gdo.core.GDT_Container import GDT_Container
from gdo.core.GDT_String import GDT_String
from gdo.core.GDT_Text import GDT_Text
from gdo.form.MethodForm import MethodForm
from gdo.markdown.MarkdownEditor import MarkdownEditor
from gdo.message.GDT_HTML import GDT_HTML
from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.mira_challs.GDO_ChallengeSolution import GDO_ChallengeSolution
from gdo.mira_challs.GDO_ChallengeSolved import GDO_ChallengeSolved


def solved_by(user, challenge):
    if not user or not user.is_authenticated() or not user.is_member() or not challenge:
        return False
    table = GDO_ChallengeSolved.table()
    return bool(table.select().where(
        f'solve_user={int(user.get_id())} AND solve_challenge={int(challenge.get_id())} '
        'AND solve_timestamp IS NOT NULL').nocache().first().exec().fetch_object())


class solutions(MethodForm):
    """Read and submit write-ups only after solving this challenge."""

    def gdo_connectors(self):
        return 'web'

    def gdo_parameters(self):
        return [GDT_String('named').not_null().positional()]

    def get_challenge(self):
        return GDO_Challenge.table().get_by_vals({'chall_name': self.param_val('named')})

    def gdo_create_form(self, form):
        form.add_field(GDT_Text('body').not_null().label('mira_challs_solution_body'))
        super().gdo_create_form(form)

    def gdo_execute(self):
        challenge = self.get_challenge()
        if not solved_by(self._env_user, challenge):
            if Application.IS_HTTP:
                Application.status('403 Forbidden')
            return self.err('err_mira_challs_solutions_forbidden')
        if Application.IS_HTTP:
            Application.header('Cache-Control', 'private, no-store')
            Application.header('X-Robots-Tag', 'noindex, nofollow')
        result = super().gdo_execute()
        if result is not self.get_form():
            return result
        container = GDT_Container().vertical()
        rows = (GDO_ChallengeSolution.table().select()
                .where(f'solution_challenge={int(challenge.get_id())}')
                .order('solution_created ASC, solution_id ASC').nocache().exec())
        for row in rows:
            author = row.gdo_value('solution_user')
            container.add_field(GDT_HTML().text(
                f"{author.render_name() if author else row.gdo_val('solution_user')} · {row.gdo_val('solution_created')}"))
            container.add_field(GDT_HTML().html(MarkdownEditor.to_html(row.gdo_val('solution_body'))))
        container.add_field(result)
        return container

    def form_submitted(self):
        challenge = self.get_challenge()
        if not solved_by(self._env_user, challenge):
            if Application.IS_HTTP:
                Application.status('403 Forbidden')
            return self.err('err_mira_challs_solutions_forbidden')
        GDO_ChallengeSolution.blank({
            'solution_challenge': challenge.get_id(),
            'solution_user': self._env_user.get_id(),
            'solution_body': self.get_form().get_field('body').get_val(),
        }).insert()
        return self.redirect_msg(href('mira_challs', 'solutions',
                                      positional=(self.param_val('named'),)),
                                 'msg_mira_challs_solution_saved')
