from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.base.util.href import href
from gdo.ui.GDT_Card import GDT_Card
from gdo.ui.GDT_Link import GDT_Link
from gdo.message.GDT_HTML import GDT_HTML
from gdo.mira_challs.GDT_AnswerBox import GDT_AnswerBox
from gdo.core.ChallengeToken import bj_secret_path, read_secret, verify
from gdo.core.GDT_Container import GDT_Container


class BJ(GDO_Challenge):
    _score = 3

    def get_challenge_tags(self) -> str:
        return 'challenge,math,fun'

    @classmethod
    def challenge_page(cls, method):
        card = GDT_Card().title('mt_mira_challs_bj')
        card.get_content().add_field(GDT_HTML().text(method.t('mc_bj_instructions', ())))
        card.get_content().add_field(GDT_Link().href(href('blackjack', 'site')).text('link_mira_challs_bj_play'))
        return GDT_Container().vertical().add_fields(card, GDT_AnswerBox(challenge_name='BJ'))

    def check_answer(self, answer):
        secret = read_secret(bj_secret_path())
        return verify(secret, 'bj1', answer)
