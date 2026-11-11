from gdo.base.Method import Method
from gdo.core.GDT_String import GDT_String
from gdo.mira_challs.GDO_Challenge import GDO_Challenge


class challenge(Method):
    def gdo_parameters(self):
        return [
            GDT_String('named').not_null().positional(),
        ]

    def gdo_execute(self):
        challenge = GDO_Challenge.load_challenge(self.param_val('named'))
        challenge.start(self._env_user)
        return challenge.challenge_page(self)
