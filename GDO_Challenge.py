from importlib import import_module
from html.parser import HTMLParser
import re

from gdo.base.GDO import GDO
from gdo.base.GDT import GDT
from gdo.base.Query import Query
from gdo.base.Trans import t, thas
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_AutoInc import GDT_AutoInc
from gdo.core.GDT_Creator import GDT_Creator
from gdo.core.GDT_Name import GDT_Name
from gdo.core.GDT_String import GDT_String
from gdo.core.GDT_UInt import GDT_UInt
from gdo.core.GDT_Virtual import GDT_Virtual
from gdo.date.GDT_Created import GDT_Created
from gdo.date.GDT_Timestamp import GDT_Timestamp
from gdo.date.Time import Time
from gdo.mira_challs.GDT_ChallSecret import GDT_ChallSecret
from gdo.ui.GDT_Score import GDT_Score


class _InfoText(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []

    def handle_data(self, data):
        self.parts.append(data)

    def handle_starttag(self, tag, attrs):
        self.parts.append(' ')

    def handle_endtag(self, tag):
        self.parts.append(' ')
from gdo.tags.WithTags import WithTags


class GDO_Challenge(WithTags, GDO):

    _score: int = 1

    def get_challenge_tags(self) -> str:
        return 'challenge'

    def get_challenge_info(self):
        key = f'mc_{type(self).__name__.lower()}_info'
        if not thas(key):
            return ''
        parser = _InfoText()
        parser.feed(t(key))
        text = ' '.join(parser.parts)
        text = re.sub(r'%(?:\([^)]+\))?[#0 +\-]*\d*(?:\.\d+)?[a-zA-Z]', '', text)
        return re.sub(r'\s+([,.;:!?])', r'\1', ' '.join(text.split()))

    def gdo_tags_table(self):
        from gdo.mira_challs.GDO_ChallengeTag import GDO_ChallengeTag
        return GDO_ChallengeTag.table()

    def gdo_tag_links_table(self):
        from gdo.mira_challs.GDO_ChallengeTagLink import GDO_ChallengeTagLink
        return GDO_ChallengeTagLink.table()

    def gdo_columns(self) -> list[GDT]:
        return [
            GDT_AutoInc('chall_id'),
            GDT_Name('chall_name').not_null().unique(),
            GDT_String('chall_description').maxlen(128),
            GDT_Score('chall_score').min(1).max(10).initial('1'),
            GDT_Virtual(GDT_UInt('chall_solvercount')).query(Query().raw(
                'SELECT COUNT(*) FROM gdo_challengesolved '
                'WHERE solve_challenge = gdo_challenge.chall_id '
                'AND solve_timestamp IS NOT NULL'
            )),
            GDT_Virtual(GDT_String('chall_last_solver')).query(Query().raw(
                "SELECT CONCAT(u.user_name, '{', LOWER(server.serv_name), '}') "
                'FROM gdo_challengesolved AS s '
                'JOIN gdo_user AS u ON u.user_id = s.solve_user '
                'JOIN gdo_server AS server ON server.serv_id = u.user_server '
                'WHERE s.solve_challenge = gdo_challenge.chall_id AND s.solve_timestamp IS NOT NULL '
                'ORDER BY s.solve_timestamp DESC, s.solve_user ASC LIMIT 1'
            )),
            GDT_Virtual(GDT_Timestamp('chall_last_solved').date_format(Time.FMT_LONG)).query(Query().raw(
                'SELECT MAX(solve_timestamp) FROM gdo_challengesolved '
                'WHERE solve_challenge = gdo_challenge.chall_id AND solve_timestamp IS NOT NULL'
            )),
            GDT_ChallSecret('chall_secret'),
            GDT_Creator('chall_creator'),
            GDT_Created('chall_created'),
        ]

    @classmethod
    def load_challenge(cls, name: str|None):
        if not isinstance(name, str) or not re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', name):
            raise ValueError('Invalid challenge name')
        module = import_module(f'gdo.mira_challs.challs.{name}.{name}')
        challenge = getattr(module, name)
        if not isinstance(challenge, type) or not issubclass(challenge, GDO_Challenge):
            raise TypeError(f'{name} is not a challenge class')
        return challenge()

    def check_answer(self, answer):
        record = GDO_Challenge.table().get_by_vals({'chall_name': type(self).__name__})
        secret_hash = record.gdo_val('chall_secret') if record else None
        if not secret_hash:
            raise NotImplementedError
        return GDT_ChallSecret.check(secret_hash, answer)

    def check_answer_for_user(self, answer, user):
        return self.check_answer(answer)

    def install_values(self):
        if not isinstance(self._score, int) or not 1 <= self._score <= 10:
            raise ValueError('Challenge score must be between 1 and 10')
        return {'chall_name': type(self).__name__, 'chall_score': self._score}

    def start(self, user: GDO_User):
        if not user.is_member():
            return None
        from gdo.mira_challs.GDO_ChallengeSolved import GDO_ChallengeSolved
        record = GDO_Challenge.table().get_by_vals({'chall_name': type(self).__name__})
        if not record:
            return None
        keys = {'solve_challenge': record.get_id(), 'solve_user': user.get_id()}
        return GDO_ChallengeSolved.table().get_by_vals(keys) or GDO_ChallengeSolved.blank(keys).insert()

    def on_solved(self, user: GDO_User):
        entry = self.start(user)
        if not entry:
            return None
        if entry.gdo_val('solve_timestamp'):
            return False
        entry.save_val('solve_timestamp', Time.get_date())
        return True
