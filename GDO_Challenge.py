from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_Creator import GDT_Creator
from gdo.date.GDT_Created import GDT_Created
from gdo.ui.GDT_Score import GDT_Score


class GDO_Challenge(GDO):
    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_AutoInc('chall_id'),
            GDT_Score('chall_score').min(1).max(10).initial('1'),
            GDT_Creator('chall_creator'),
            GDT_Created('chall_created'),
        ]
