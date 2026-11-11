from gdo.base.util.href import href
from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.table.MethodQueryTable import MethodQueryTable
from gdo.ui.GDT_Link import GDT_Link


class challenges(MethodQueryTable):
    def gdo_needs_authentication(self) -> bool:
        return False

    def gdo_table(self):
        return GDO_Challenge.table()

    def gdo_table_headers(self):
        columns = self.gdo_table().columns()
        return [columns['chall_name'], columns['chall_score']]

    def gdo_order_default(self):
        return 'chall_name ASC'

    def render_chall_name(self, field, challenge):
        name = challenge.gdo_val('chall_name')
        return GDT_Link().href(
            href('mira_challs', 'challenge', positional=(name,))
        ).text_raw(name).icon(None).render_html()
