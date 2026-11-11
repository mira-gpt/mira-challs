from gdo.base.util.href import href
from gdo.form.GDT_Form import GDT_Form
from urllib.parse import urlencode


class GDT_AnswerBox(GDT_Form):
    def __init__(self, name='answerbox', method=None, challenge_name=None):
        super().__init__(name)
        if method is None:
            from gdo.mira_challs.method.solve import solve
            method = solve()
        args = urlencode({'named': challenge_name}) if challenge_name else ''
        self.href(href('mira_challs', 'solve', args))
        self.method(method)
        method.gdo_create_form(self)
