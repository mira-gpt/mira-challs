from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.base.util.href import href
from gdo.ui.GDT_Card import GDT_Card
from gdo.ui.GDT_Link import GDT_Link


class BJ(GDO_Challenge):
    @classmethod
    def challenge_page(cls, method):
        card = GDT_Card().title('mt_mira_challs_bj')
        card.get_content().add_field(GDT_Link().href(href('blackjack', 'site')).text('link_mira_challs_bj_play'))
        return card

    def check_answer(self, answer):
        pass
        # TODO: Do the hashing like in gwf3 version
