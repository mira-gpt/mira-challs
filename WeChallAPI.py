"""The inbound WeChall account-validation and challenge-score protocol."""
import re

from gdo.base.Application import Application
from gdo.base.GDT import GDT
from gdo.core.GDO_User import GDO_User
from gdo.core.GDT_Password import GDT_Password
from gdo.mira_challs.module_mira_challs import module_mira_challs


def authorized(authkey):
    module = module_mira_challs.instance()
    if not module.get_config_value('wechall_enabled'):
        return False
    stored = module.get_config_val('wechall_authkey')
    if not stored or not isinstance(authkey, str) or not authkey or len(authkey.encode('utf-8')) > 72:
        return False
    try:
        return GDT_Password.check(stored, authkey)
    except (ValueError, TypeError):
        return False


def resolve_onsite_user(onsitename):
    """Resolve exact nick{server} and follow valid links to the shared user."""
    if not isinstance(onsitename, str) or len(onsitename) > 192:
        return None
    match = re.fullmatch(r'([^{}]+)\{([^{}]+)\}', onsitename)
    if not match:
        return None
    nick, server = match.groups()
    query = GDO_User.table().select('gdo_user.*').join(
        'JOIN gdo_server ON gdo_server.serv_id = gdo_user.user_server'
    ).where(f'BINARY gdo_user.user_name = BINARY {GDT.quote(nick)}').where(
        f'BINARY LOWER(gdo_server.serv_name) = BINARY {GDT.quote(server)}'
    ).limit(2).nocache()
    rows = query.exec().fetch_all()._items
    if len(rows) != 1:
        return None
    user, seen = rows[0], set()
    while user:
        user_id = user.get_id()
        if not user_id or user_id in seen:
            return None
        seen.add(user_id)
        if not user.gdo_val('user_link'):
            return user if user.is_member() else None
        user = user.get_linked_user()
    return None


def validate_account(onsitename, email):
    if not isinstance(email, str) or not email:
        return False
    user = resolve_onsite_user(onsitename)
    return bool(user and user.get_mail() == email)


def score_for(onsitename):
    user = resolve_onsite_user(onsitename)
    if user is None:
        return None
    db = Application.db()
    score = db.select(
        'SELECT COALESCE(SUM(c.chall_score), 0) FROM gdo_challengesolved AS s '
        'JOIN gdo_challenge AS c ON c.chall_id = s.solve_challenge '
        f'WHERE s.solve_user = {int(user.get_id())} AND s.solve_timestamp IS NOT NULL'
    ).fetch_val()
    maximum = db.select('SELECT COALESCE(SUM(chall_score), 0) FROM gdo_challenge').fetch_val()
    challenge_count = db.select('SELECT COUNT(*) FROM gdo_challenge').fetch_val()
    user_count = db.select(
        'SELECT COUNT(DISTINCT s.solve_user) FROM gdo_challengesolved AS s '
        'JOIN gdo_challenge AS c ON c.chall_id = s.solve_challenge '
        'WHERE s.solve_timestamp IS NOT NULL'
    ).fetch_val()
    return int(score or 0), int(maximum or 0), int(challenge_count or 0), int(user_count or 0)
