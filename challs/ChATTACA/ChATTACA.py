from gdo.core.GDT_Container import GDT_Container
from gdo.message.GDT_HTML import GDT_HTML
from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.ui.GDT_Card import GDT_Card


class ChATTACA(GDO_Challenge):
    @classmethod
    def challenge_page(cls, method):
        card = GDT_Card().title('mc_chattaca_title')
        card.get_content().add_field(GDT_HTML().html(method.t('mc_chattaca_info', ())))
        return GDT_Container().vertical().add_field(card)
