from gdo.base.Application import Application
from gdo.base.Method import Method
from gdo.core.GDT_Raw import GDT_Raw
from gdo.core.GDT_String import GDT_String
from gdo.mira_challs.WeChallAPI import authorized, validate_account


class wechall_validate(Method):
    def gdo_connectors(self):
        return 'web'

    def gdo_needs_authentication(self):
        return False

    def gdo_parameters(self):
        return [GDT_String('username').maxlen(192),
                GDT_String('email').maxlen(254),
                GDT_String('authkey').maxlen(72).secret()]

    def gdo_execute(self):
        Application.header('Cache-Control', 'no-store')
        valid = (authorized(self.param_val('authkey', False)) and
                 validate_account(self.param_val('username', False), self.param_val('email', False)))
        return GDT_Raw('result').val('1' if valid else '0')
