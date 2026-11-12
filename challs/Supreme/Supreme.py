"""Supreme, adapted from the GWF3 challenge."""
from html import escape
from pathlib import Path

from gdo.core.GDT_Container import GDT_Container
from gdo.message.GDT_HTML import GDT_HTML
from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.mira_challs.GDT_AnswerBox import GDT_AnswerBox
from gdo.mira_challs.GDT_ChallSecret import GDT_ChallSecret
from gdo.ui.GDT_Card import GDT_Card


def secret_answer():
    answer = Path(__file__).with_name('secret_answer').read_text(encoding='utf-8').strip()
    if not answer or len(answer.encode('utf-8')) > 72:
        raise ValueError('Supreme answer is missing or too long for bcrypt')
    return answer


class Supreme(GDO_Challenge):
    _score = 3

    def install_values(self):
        return {**super().install_values(), 'chall_secret': GDT_ChallSecret.hash(secret_answer())}

    def check_answer(self, answer):
        if not isinstance(answer, str) or len(answer.encode('utf-8')) > 72:
            return False
        return super().check_answer(answer)

    @classmethod
    def challenge_page(cls, method):
        username = escape(method._env_user.get_name())
        profile = 'https://backend.www.linkuup.de/user.profile.for.shqiprim.html'
        card = GDT_Card().title('mc_supreme_title')
        card.get_content().add_field(GDT_HTML().html(method.t('mc_supreme_info', (username, profile)).replace('\n', '<br>\n')))
        return GDT_Container().vertical().add_fields(card, GDT_AnswerBox(challenge_name='Supreme'))
