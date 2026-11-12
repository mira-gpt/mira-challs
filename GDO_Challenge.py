from importlib import import_module
import re

from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_Creator import GDT_Creator
from gdo.core.GDT_Name import GDT_Name
from gdo.date.GDT_Created import GDT_Created
from gdo.date.Time import Time
from gdo.mira_challs.GDT_ChallSecret import GDT_ChallSecret
from gdo.ui.GDT_Score import GDT_Score


class GDO_Challenge(GDO):
    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_AutoInc('chall_id'),
            GDT_Name('chall_name').not_null().unique(),
            GDT_Score('chall_score').min(1).max(10).initial('1'),
            GDT_ChallSecret('chall_secret'),
            GDT_Creator('chall_creator'),
            GDT_Created('chall_created'),
        ]

    @classmethod
    def load_challenge(cls, name: str|None):
        if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', name):
            raise ValueError('Invalid challenge name')
        module = import_module(f'gdo.mira_challs.challs.{name}.{name}')
        challenge = getattr(module, name)
        if not isinstance(challenge, type) or not issubclass(challenge, GDO_Challenge):
            raise TypeError(f'{name} is not a challenge class')
        return challenge()

    def check_answer(self, answer):
        record = GDO_Challenge.table().get_by_vals({'chall_name': type(self).__name__})
        secret_hash = record.gdo_val('chall_secret') if record else None
        if not secret_hash:
            raise NotImplementedError
        return GDT_ChallSecret.check(secret_hash, answer)

    def start(self, user: GDO_User):
        if not user.is_member():
            return None
        from gdo.mira_challs.GDO_ChallengeSolved import GDO_ChallengeSolved
        record = GDO_Challenge.table().get_by_vals({'chall_name': type(self).__name__})
        if not record:
            return None
        keys = {'solve_challenge': record.get_id(), 'solve_user': user.get_id()}
        return GDO_ChallengeSolved.table().get_by_vals(keys) or GDO_ChallengeSolved.blank(keys).insert()

    def on_solved(self, user: GDO_User):
        entry = self.start(user)
        if not entry:
            return None
        if entry.gdo_val('solve_timestamp'):
            return False
        entry.save_val('solve_timestamp', Time.get_date())
        return True
