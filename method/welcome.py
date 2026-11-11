from gdo.base.Method import Method
from gdo.message.GDT_HTML import GDT_HTML
from gdo.ui.GDT_Card import GDT_Card


class welcome(Method):
    @classmethod
    def gdo_trigger(cls):
        return 'mira_challenges.welcome'

    def gdo_execute(self):
        card = GDT_Card().title('mt_mira_challs_welcome')
        card.get_content().add_field(GDT_HTML().html(self.t('msg_mira_challs_welcome', ())))
        return card
