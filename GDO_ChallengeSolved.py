from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.core.GDT_Object import GDT_Object
from gdo.core.GDT_User import GDT_User
from gdo.date.GDT_Created import GDT_Created
from gdo.date.GDT_Timestamp import GDT_Timestamp
from gdo.mira_challs.GDO_Challenge import GDO_Challenge


class GDO_ChallengeSolved(GDO):
    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_Object('solve_challenge').table(GDO_Challenge.table()).primary(),
            GDT_User('solve_user').primary(),
            GDT_Timestamp('solve_timestamp'),
            GDT_Created('solve_created'),
        ]
