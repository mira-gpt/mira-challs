from gdo.base.util.href import href
from gdo.base.Result import ResultType
from gdo.core.GDT_Container import GDT_Container
from gdo.core.GDT_UInt import GDT_UInt
from gdo.core.GDT_String import GDT_String
from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.mira_challs.GDO_ChallengeTag import GDO_ChallengeTag
from gdo.mira_challs.GDO_ChallengeTagLink import GDO_ChallengeTagLink
from gdo.table.MethodQueryTable import MethodQueryTable
from gdo.tags.GDT_TagCloud import GDT_TagCloud
from gdo.ui.GDT_Link import GDT_Link


class challenges(MethodQueryTable):
    def gdo_needs_authentication(self) -> bool:
        return False

    def gdo_searched(self) -> bool:
        return False

    def gdo_table(self):
        return GDO_Challenge.table()

    def gdo_parameters(self):
        return [GDT_UInt('tag').min(1)]

    def tag_cloud(self):
        tags = GDO_ChallengeTag.table()
        links = GDO_ChallengeTagLink.table()
        tag_table, link_table = tags.gdo_table_name(), links.gdo_table_name()
        rows = tags.select(f'{tag_table}.tag_id, {tag_table}.tag_name, COUNT(*)') \
            .join(f'JOIN {link_table} ON {link_table}.tag_id = {tag_table}.tag_id') \
            .group(f'{tag_table}.tag_id, {tag_table}.tag_name') \
            .order(f'{tag_table}.tag_name ASC').exec(False).iter(ResultType.ROW)
        selected = self.param_value('tag', throw=False)
        return GDT_TagCloud().entries(
            rows, lambda key: href('mira_challs', 'challenges', append=f'tag={key}'),
            selected=selected, clear_href=href('mira_challs', 'challenges'),
            clear_label=self.t('mira_challs_all_tags', ()))

    def gdo_execute(self):
        return GDT_Container().vertical().add_fields(self.tag_cloud(), super().gdo_execute())

    def gdo_table_headers(self):
        columns = self.gdo_table().columns()
        headers = [columns['chall_name'], columns['chall_score'], columns['chall_solvercount'],
                columns['chall_created'].copy_as().label('chall_age'),
                columns['chall_last_solver'], columns['chall_last_solved']]
        user = getattr(self, '_env_user', None)
        if user and user.is_authenticated() and user.has_permission('owner'):
            headers.append(GDT_String('edit_action').label('mira_challs_edit_action'))
            headers.append(GDT_String('reinstall_action').label('mira_challs_reinstall_action'))
        return headers

    def render_edit_action(self, field, challenge):
        return GDT_Link().href(href('mira_challs', 'edit', positional=(challenge.gdo_val('chall_name'),))).text('mira_challs_edit_action').render_html()

    def render_reinstall_action(self, field, challenge):
        return GDT_Link().href(href('mira_challs', 'reinstall_one', positional=(challenge.gdo_val('chall_name'),))).text('mira_challs_reinstall_action').render_html()

    def gdo_table_query(self):
        # A started attempt has no timestamp and is not a solve. Do not cache
        # result objects containing this derived value: it changes independently.
        table = self.gdo_table()
        query = table.select()
        if tag := self.param_value('tag', throw=False):
            links = GDO_ChallengeTagLink.gdo_table_name()
            query.where(f'{table.gdo_table_name()}.chall_id IN '
                        f'(SELECT obj_id FROM {links} WHERE tag_id = {int(tag)})')
        for name in ('chall_solvercount', 'chall_last_solver', 'chall_last_solved'):
            table.column(name).select_into(query)
        return query.nocache()

    def gdo_order_default(self):
        return 'chall_name ASC'

    def render_chall_name(self, field, challenge):
        name = challenge.gdo_val('chall_name')
        return GDT_Link().href(
            href('mira_challs', 'challenge', positional=(name,))
        ).text_raw(name).icon(None).render_html()
