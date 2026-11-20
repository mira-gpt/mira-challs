from gdo.base.GDO import GDO
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_Object import GDT_Object
from gdo.core.GDT_Text import GDT_Text
from gdo.core.GDT_User import GDT_User
from gdo.date.GDT_Created import GDT_Created
from gdo.mira_challs.GDO_Challenge import GDO_Challenge


class GDO_ChallengeSolution(GDO):
    """One Markdown write-up; a solver can submit more than one per challenge."""

    def gdo_columns(self):
        return [
            GDT_AutoInc('solution_id'),
            GDT_Object('solution_challenge').table(GDO_Challenge.table()).not_null(),
            GDT_User('solution_user').not_null(),
            GDT_Text('solution_body').not_null(),
            GDT_Created('solution_created'),
        ]
