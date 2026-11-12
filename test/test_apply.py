import unittest
from unittest.mock import MagicMock, patch

from gdo.mira_challs.challs.APPLY.APPLY import APPLY
from gdo.mira_challs.method.apply_approve import apply_approve


class ApplyTest(unittest.TestCase):
    def test_page_shows_admin_link_only_to_admin(self):
        method = MagicMock()
        method.t.return_value = '<p>Apply</p>'
        method._env_user.is_admin.return_value = False
        with patch('gdo.mira_challs.challs.APPLY.APPLY.href', return_value='/approve'):
            self.assertEqual(1, len(APPLY.challenge_page(method).get_fields()))
            method._env_user.is_admin.return_value = True
            self.assertEqual(2, len(APPLY.challenge_page(method).get_fields()))

    def test_only_admin_can_access_web_approval(self):
        with patch('gdo.base.Application.Application.get_mode', return_value=None):
            method = apply_approve()
        self.assertEqual('admin', method.gdo_user_permission())
        self.assertEqual('web', method.gdo_connectors())

    def test_review_result(self):
        with patch('gdo.base.Application.Application.get_mode', return_value=None):
            method = apply_approve()
        user = MagicMock()
        method.param_value = MagicMock(return_value=user)
        method.msg = MagicMock(side_effect=lambda key: key)
        method.err = MagicMock(side_effect=lambda key: key)
        with patch('gdo.mira_challs.method.apply_approve.APPLY.on_solved') as solved:
            for result, expected in ((True, 'msg_mira_challs_apply_approved'),
                                     (False, 'msg_mira_challs_apply_already_solved'),
                                     (None, 'err_mira_challs_apply_unavailable')):
                solved.return_value = result
                self.assertEqual(expected, method.form_submitted())
                solved.assert_called_with(user)
