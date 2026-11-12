from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.base.util.href import href
from gdo.core.GDT_Container import GDT_Container
from gdo.message.GDT_HTML import GDT_HTML
from gdo.ui.GDT_Card import GDT_Card
from gdo.ui.GDT_Link import GDT_Link


class APPLY(GDO_Challenge):
    @classmethod
    def challenge_page(cls, method):
        card = GDT_Card().title('mc_apply_title')
        card.get_content().add_field(GDT_HTML().html(method.t('mc_apply_info', ())))
        page = GDT_Container().vertical().add_field(card)
        if method._env_user.is_admin():
            page.add_field(GDT_Link().href(href('mira_challs', 'apply_approve')).text('mt_mira_challs_apply_approve'))
        return page
