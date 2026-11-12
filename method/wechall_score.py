from gdo.base.Application import Application
from gdo.base.Method import Method
from gdo.core.GDT_Raw import GDT_Raw
from gdo.core.GDT_String import GDT_String
from gdo.mira_challs.WeChallAPI import authorized, score_for


class wechall_score(Method):
    def gdo_connectors(self):
        return 'web'

    def gdo_needs_authentication(self):
        return False

    def gdo_parameters(self):
        return [GDT_String('username').maxlen(192),
                GDT_String('authkey').maxlen(72).secret()]

    def gdo_execute(self):
        Application.header('Cache-Control', 'no-store')
        score = score_for(self.param_val('username', False)) if authorized(self.param_val('authkey', False)) else None
        return GDT_Raw('result').val(':'.join(map(str, score)) if score is not None else '0')
