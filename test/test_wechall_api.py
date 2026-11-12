import unittest
from unittest.mock import MagicMock, patch

from gdo.core.GDT_Password import GDT_Password
from gdo.mira_challs import WeChallAPI as api
from gdo.mira_challs.method.wechall_score import wechall_score
from gdo.mira_challs.method.wechall_validate import wechall_validate


class WeChallAPITest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.key_hash = GDT_Password.hash('synthetic-key')

    def test_authkey_required_and_disabled_by_default(self):
        module = MagicMock()
        module.get_config_value.return_value = False
        module.get_config_val.return_value = self.key_hash
        with patch.object(api.module_mira_challs, 'instance', return_value=module):
            self.assertFalse(api.authorized('synthetic-key'))
            module.get_config_value.return_value = True
            self.assertFalse(api.authorized('wrong'))
            self.assertFalse(api.authorized(None))
            self.assertTrue(api.authorized('synthetic-key'))

    def test_exact_qualified_user_and_link_resolution(self):
        origin, target = MagicMock(), MagicMock()
        origin.get_id.return_value = '11'
        origin.gdo_val.return_value = '12'
        origin.get_linked_user.return_value = target
        target.get_id.return_value = '12'
        target.gdo_val.return_value = None
        target.is_member.return_value = True
        table = MagicMock()
        query = table.select.return_value
        query.join.return_value = query.where.return_value = query.limit.return_value = query.nocache.return_value = query
        query.exec.return_value.fetch_all.return_value._items = [origin]
        with patch.object(api.GDO_User, 'table', return_value=table):
            self.assertIsNone(api.resolve_onsite_user('nickname'))
            self.assertIs(api.resolve_onsite_user('nickname{server}'), target)
            conditions = [call.args[0] for call in query.where.call_args_list]
            self.assertTrue(all('BINARY' in condition for condition in conditions))
            query.exec.return_value.fetch_all.return_value._items = [origin, target]
            self.assertIsNone(api.resolve_onsite_user('nickname{server}'))
            query.exec.return_value.fetch_all.return_value._items = [origin]
            target.gdo_val.return_value = '11'
            target.get_linked_user.return_value = origin
            self.assertIsNone(api.resolve_onsite_user('nickname{server}'))

    def test_email_is_confirmed_and_case_sensitive(self):
        user = MagicMock()
        user.get_mail.return_value = 'A@example.test'
        with patch.object(api, 'resolve_onsite_user', return_value=user):
            self.assertTrue(api.validate_account('x{web}', 'A@example.test'))
            self.assertFalse(api.validate_account('x{web}', 'a@example.test'))
        user.get_mail.assert_called_with()

    def test_score_counts_only_completed_solves(self):
        user = MagicMock()
        user.get_id.return_value = '42'
        db = MagicMock()
        db.select.side_effect = [MagicMock(fetch_val=MagicMock(return_value=value))
                                 for value in (3, 10, 2, 4)]
        with patch.object(api, 'resolve_onsite_user', return_value=user), \
             patch.object(api.Application, 'db', return_value=db):
            self.assertEqual((3, 10, 2, 4), api.score_for('x{web}'))
        self.assertIn('s.solve_timestamp IS NOT NULL', db.select.call_args_list[0].args[0])
        self.assertIn('COUNT(DISTINCT s.solve_user)', db.select.call_args_list[3].args[0])
        self.assertIn('s.solve_timestamp IS NOT NULL', db.select.call_args_list[3].args[0])

    def test_endpoint_fails_closed(self):
        with patch('gdo.base.Application.Application.get_mode', return_value=None):
            for cls in (wechall_validate, wechall_score):
                method = cls()
                method.param_val = MagicMock(return_value='bad-key')
                with patch('gdo.base.Application.Application.header'), \
                     patch('gdo.mira_challs.method.' + cls.__name__ + '.authorized', return_value=False):
                    self.assertEqual('0', method.gdo_execute().render_txt())

    def test_endpoints_return_plain_protocol_values(self):
        with patch('gdo.base.Application.Application.get_mode', return_value=None), \
             patch('gdo.base.Application.Application.header'):
            validate = wechall_validate()
            validate.param_val = MagicMock(side_effect=lambda name, _throw: {
                'authkey': 'key', 'username': 'Ada{web}', 'email': 'ada@example.test'
            }[name])
            with patch('gdo.mira_challs.method.wechall_validate.authorized', return_value=True), \
                 patch('gdo.mira_challs.method.wechall_validate.validate_account', return_value=True):
                self.assertEqual('1', validate.gdo_execute().render_txt())
            score = wechall_score()
            score.param_val = MagicMock(side_effect=lambda name, _throw: {
                'authkey': 'key', 'username': 'Ada{web}'
            }[name])
            with patch('gdo.mira_challs.method.wechall_score.authorized', return_value=True), \
                 patch('gdo.mira_challs.method.wechall_score.score_for', return_value=(3, 10, 2, 4)):
                self.assertEqual('3:10:2:4', score.gdo_execute().render_txt())
