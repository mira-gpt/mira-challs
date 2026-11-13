"""A deterministic reading-and-bookkeeping puzzle, not a bot detector."""
import re
import hashlib
from html import escape

from gdo.core.GDT_Container import GDT_Container
from gdo.message.GDT_HTML import GDT_HTML
from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.mira_challs.GDT_AnswerBox import GDT_AnswerBox
from gdo.ui.GDT_Card import GDT_Card


def starting_values(user_id) -> str:
    user_id = str(user_id)
    if not re.fullmatch(r'[0-9]+', user_id):
        raise ValueError('Invalid user ID')
    digest = hashlib.sha256(('pobab-v1:' + user_id).encode('ascii')).digest()
    return ''.join(str(value % 10) for value in digest[:16])


def solution(user_id) -> str:
    lockers = dict(zip('ABCDEFGHIJKLMNOP', map(int, starting_values(user_id))))

    def swap(a, b):
        lockers[a], lockers[b] = lockers[b], lockers[a]

    swap('A', 'P')
    swap('C', 'M')
    swap('F', 'J')
    lockers['B'] = (lockers['B'] + lockers['A']) % 10
    lockers['D'] = (lockers['D'] + lockers['C']) % 10
    lockers['H'] = (lockers['H'] + lockers['G']) % 10
    swap('E', 'N' if lockers['B'] % 2 == 0 else 'O')
    swap('K', 'L' if lockers['D'] > lockers['H'] else 'I')
    lockers['P'] = (lockers['P'] + lockers['B'] + lockers['D']) % 10
    lockers['M'] = (lockers['M'] + lockers['F'] + lockers['J']) % 10
    swap('A', 'H')
    swap('B', 'G')
    swap('C', 'F')
    swap('D', 'E')
    lockers['I'] = (lockers['I'] + lockers['P']) % 10
    lockers['N'] = (lockers['N'] + lockers['M']) % 10
    swap('O', 'P')
    lockers['J'] = (lockers['J'] + lockers['I'] + lockers['N']) % 10
    return ''.join(str(lockers[name]) for name in 'ABCDEFGHIJKLMNOP')


class POBAB(GDO_Challenge):

    def get_challenge_tags(self) -> str:
        return 'challenge,coding'

    def check_answer_for_user(self, answer, user):
        if not isinstance(answer, str):
            return False
        answer = answer.strip()
        return bool(re.fullmatch(r'[0-9]{16}', answer) and answer == solution(user.get_id()))

    @classmethod
    def challenge_page(cls, method):
        username = escape(method._env_user.get_name())
        values = starting_values(method._env_user.get_id())
        labels = ', '.join(f'{name}={value}' for name, value in zip('ABCDEFGHIJKLMNOP', values))
        card = GDT_Card().title('mc_pobab_title')
        card.get_content().add_field(GDT_HTML().html(
            method.t('mc_pobab_info', (username, labels)).replace('\n', '<br>\n')))
        return GDT_Container().vertical().add_fields(card, GDT_AnswerBox(challenge_name='POBAB'))
