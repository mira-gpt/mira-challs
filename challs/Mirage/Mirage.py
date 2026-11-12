"""Mirage: the GWF3 investigation challenge adapted for Mira Challs."""
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
    if not answer or len(answer.lower().encode('utf-8')) > 72:
        raise ValueError('Mirage answer is missing or too long for bcrypt')
    return answer.lower()


class Mirage(GDO_Challenge):
    def install_values(self):
        return {'chall_name': type(self).__name__,
                'chall_secret': GDT_ChallSecret.hash(secret_answer())}

    def check_answer(self, answer):
        if not isinstance(answer, str) or len(answer.lower().encode('utf-8')) > 72:
            return False
        return super().check_answer(answer.lower())

    @classmethod
    def challenge_page(cls, method):
        username = escape(method._env_user.get_name())
        card = GDT_Card().title('mc_mirage_title')
        info = method.t('mc_mirage_info', (username, 'https://mogwai.mira-gpt.org/',
                                            'https://youtu.be/Pgmx7z49OEk'))
        card.get_content().add_field(GDT_HTML().html(info))
        return GDT_Container().vertical().add_fields(card, GDT_AnswerBox(challenge_name='Mirage'))
