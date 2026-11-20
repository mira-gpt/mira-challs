from gdo.base.Method import Method
from gdo.base.Trans import t, thas
from gdo.core.GDT_String import GDT_String
from gdo.core.GDT_Container import GDT_Container
from gdo.base.util.href import href
from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.mira_challs.method.solutions import solved_by
from gdo.ui.GDT_Link import GDT_Link
from html import escape


class challenge(Method):
    def gdo_parameters(self):
        return [
            GDT_String('named').not_null().positional(),
        ]

    def gdo_execute(self):
        challenge = GDO_Challenge.load_challenge(self.param_val('named'))
        challenge.start(self._env_user)
        result = challenge.challenge_page(self)
        record = GDO_Challenge.table().get_by_vals({'chall_name': self.param_val('named')})
        if solved_by(self._env_user, record):
            link = GDT_Link().href(href('mira_challs', 'solutions',
                                       positional=(self.param_val('named'),))).text('mt_mira_challs_solutions')
            return GDT_Container().vertical().add_fields(result, link)
        return result

    def gdo_render_descr(self):
        name = self.param_val('named', throw=False)
        try:
            chall = GDO_Challenge.load_challenge(name)
            info = chall.get_challenge_info()[:160].strip()
            title_key = f'mc_{name.lower()}_title'
            title = t(title_key) if thas(title_key) else name
            return escape(t('md_mira_challs_challenge', (title, info)), quote=True)
        except (ImportError, AttributeError, TypeError, ValueError):
            return escape(t('md_mira_challs_challenge_fallback'), quote=True)
