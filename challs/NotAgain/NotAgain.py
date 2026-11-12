"""A separator-free Morse puzzle, inspired by the GWF3 challenge."""
import hashlib
import re
from pathlib import Path

from gdo.core.GDT_Container import GDT_Container
from gdo.message.GDT_HTML import GDT_HTML
from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.mira_challs.GDT_AnswerBox import GDT_AnswerBox
from gdo.mira_challs.GDT_ChallSecret import GDT_ChallSecret
from gdo.ui.GDT_Card import GDT_Card

MORSE = dict(zip('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,?:;!-/@()&=+',
                 '.- -... -.-. -.. . ..-. --. .... .. .--- -.- .-.. -- -. --- .--. --.- .-. ... - ..- ...- .-- -..- -.-- --.. ----- .---- ..--- ...-- ....- ..... -.... --... ---.. ----. .-.-.- --..-- ..--.. ---... -.-.-. -.-.-- -....- -..-. .--.-. -.--. -.--.- .-... -...- .-.-.'.split()))


def plaintext():
    return Path(__file__).with_name('secret_plaintext').read_text(encoding='utf-8')


def compatible(text):
    return ''.join(char for char in text.upper() if char in MORSE or char == ' ')


def expected_answer(text):
    return hashlib.sha512(compatible(text).replace(' ', '').encode()).hexdigest().upper()


def bcrypt_input(answer):
    return hashlib.sha256(answer.encode('ascii')).hexdigest()


class NotAgain(GDO_Challenge):
    _score = 8

    def install_values(self):
        return {**super().install_values(),
                'chall_secret': GDT_ChallSecret.hash(bcrypt_input(expected_answer(plaintext())))}

    def check_answer(self, answer):
        if not isinstance(answer, str) or not re.fullmatch(r'[0-9A-F]{128}', answer):
            return False
        return super().check_answer(bcrypt_input(answer))

    @classmethod
    def challenge_page(cls, method):
        encoded = ''.join(MORSE.get(char, '') for char in compatible(plaintext()))
        card = GDT_Card().title('mc_notagain_title')
        card.get_content().add_field(GDT_HTML().html(method.t('mc_notagain_info', (encoded,))))
        return GDT_Container().vertical().add_fields(card, GDT_AnswerBox(challenge_name='NotAgain'))
