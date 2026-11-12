"""Error correction puzzle based on the original GWF3 draft."""
import hashlib
import re
from html import escape
from pathlib import Path

from gdo.core.GDT_Container import GDT_Container
from gdo.message.GDT_HTML import GDT_HTML
from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.mira_challs.GDT_AnswerBox import GDT_AnswerBox
from gdo.mira_challs.GDT_ChallSecret import GDT_ChallSecret
from gdo.ui.GDT_Card import GDT_Card


def secret_text(name):
    return Path(__file__).with_name(name).read_text(encoding='utf-8')


def expected_answer(text):
    letters = re.sub(r'[^a-zA-Z]', '', text).lower()
    return hashlib.sha512(letters.encode('ascii')).hexdigest()


def bcrypt_input(answer):
    return hashlib.sha256(answer.encode('ascii')).hexdigest()


class Errection(GDO_Challenge):
    _score = 2

    def install_values(self):
        answer = expected_answer(secret_text('secret_plaintext'))
        return {**super().install_values(), 'chall_secret': GDT_ChallSecret.hash(bcrypt_input(answer))}

    def check_answer(self, answer):
        if not isinstance(answer, str) or not re.fullmatch(r'[0-9a-f]{128}', answer):
            return False
        return super().check_answer(bcrypt_input(answer))

    @classmethod
    def challenge_page(cls, method):
        message = escape(secret_text('secret_message'))
        card = GDT_Card().title('mc_errection_title')
        card.get_content().add_field(GDT_HTML().html(method.t('mc_errection_info', (message,))))
        return GDT_Container().vertical().add_fields(card, GDT_AnswerBox(challenge_name='Errection'))
