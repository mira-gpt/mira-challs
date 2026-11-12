import unittest
from unittest.mock import MagicMock, patch

from gdo.mira_challs.challs.ChATTACA.ChATTACA import ChATTACA
from gdo.mira_challs.method.chattaca_approve import chattaca_approve


class ChattacaTest(unittest.TestCase):
    def test_page_has_html_and_no_answer_box(self):
        method = MagicMock()
        method.t.return_value = '<p>Talk to Mira</p>'
        page = ChATTACA.challenge_page(method)
        self.assertEqual(1, len(page.get_fields()))
        self.assertEqual('<p>Talk to Mira</p>',
                         page.get_fields()[0].get_content().get_fields()[0].render_html())

    def test_approval_is_authenticated_owner_tcp(self):
        with patch('gdo.base.Application.Application.get_mode', return_value=None):
            method = chattaca_approve()
        self.assertEqual('tcp', method.gdo_connectors())
        self.assertEqual('owner', method.gdo_user_permission())
        self.assertTrue(method.gdo_needs_authentication())

    def test_approval_results(self):
        with patch('gdo.base.Application.Application.get_mode', return_value=None):
            method = chattaca_approve()
        user = MagicMock()
        method.param_value = MagicMock(return_value=user)
        method.msg = MagicMock(side_effect=lambda key, args: key)
        method.err = MagicMock(side_effect=lambda key: key)
        with patch('gdo.mira_challs.method.chattaca_approve.ChATTACA.on_solved') as solved:
            for result, expected in ((True, 'msg_mira_challs_chattaca_approved'),
                                     (False, 'msg_mira_challs_chattaca_already'),
                                     (None, 'err_mira_challs_chattaca_unavailable')):
                solved.return_value = result
                self.assertEqual(expected, method.gdo_execute())
                solved.assert_called_with(user)
