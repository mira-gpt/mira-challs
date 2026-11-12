from urllib.parse import urlencode

from gdo.base.util.href import href
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_String import GDT_String
from gdo.core.GDT_UInt import GDT_UInt
from gdo.table.MethodQueryTable import MethodQueryTable
from gdo.ui.GDT_Link import GDT_Link
from gdo.ui.GDT_Rank import GDT_Rank


class ranking(MethodQueryTable):
    """Rank accounts by points from completed challenges."""

    def gdo_needs_authentication(self):
        return False

    def gdo_table(self):
        return GDO_User.table()

    def gdo_filtered(self):
        return False

    def gdo_searched(self):
        return False

    def gdo_ordered(self):
        return False

    def gdo_table_headers(self):
        return [GDT_Rank('rank'), GDT_String('user_name').label('mira_challs_ranking_user'),
                GDT_UInt('chall_points').label('mira_challs_ranking_points'),
                GDT_UInt('chall_solved').label('mira_challs_ranking_solved')]

    def gdo_table_query(self):
        return (self.gdo_table().select('gdo_user.*')
                .select('gdo_server.serv_name AS ranking_server')
                .select('(SELECT COALESCE(SUM(c.chall_score), 0) FROM gdo_challengesolved AS s '
                        'JOIN gdo_challenge AS c ON c.chall_id = s.solve_challenge '
                        'WHERE s.solve_user = gdo_user.user_id AND s.solve_timestamp IS NOT NULL) AS chall_points')
                .select('(SELECT COUNT(*) FROM gdo_challengesolved AS s '
                        'JOIN gdo_challenge AS c ON c.chall_id = s.solve_challenge '
                        'WHERE s.solve_user = gdo_user.user_id AND s.solve_timestamp IS NOT NULL) AS chall_solved')
                .join('JOIN gdo_server ON gdo_server.serv_id = gdo_user.user_server')
                .where('EXISTS (SELECT 1 FROM gdo_challengesolved AS s '
                       'JOIN gdo_challenge AS c ON c.chall_id = s.solve_challenge '
                       'WHERE s.solve_user = gdo_user.user_id AND s.solve_timestamp IS NOT NULL)')
                .order('chall_points DESC, gdo_user.user_id ASC')
                .nocache())

    def render_rank(self, _field, _user):
        self._curr_table_row_id += 1
        return str(self._curr_table_row_id)

    def render_user_name(self, _field, user):
        name = f"{user.gdo_val('user_name')}{{{user.gdo_val('ranking_server').lower()}}}"
        params = urlencode({'for': f'{user.get_id()}-{name}'})
        return GDT_Link().href(href('user', 'profile', params)).text_raw(name).icon(None).render_html()
