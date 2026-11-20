import unittest
from unittest.mock import MagicMock, patch

from gdo.base.Application import Application
from gdo.form.MethodForm import MethodForm
from gdo.markdown.MarkdownEditor import MarkdownEditor
from gdo.mira_challs.GDO_ChallengeSolution import GDO_ChallengeSolution
from gdo.mira_challs.method.solutions import solutions, solved_by
from gdo.mira_challs.module_mira_challs import module_mira_challs


class ChallengeSolutionsTest(unittest.TestCase):
    def test_model_and_dependency(self):
        module = module_mira_challs()
        self.assertIn('markdown', module.gdo_dependencies())
        self.assertIn(GDO_ChallengeSolution, module.gdo_classes())
        with patch.object(Application, 'get_mode', return_value=None), \
             patch('gdo.mira_challs.GDO_Challenge.GDO_Challenge.table'), \
             patch('gdo.core.GDO_User.GDO_User.table'):
            columns = GDO_ChallengeSolution().gdo_columns()
        self.assertEqual(['solution_id', 'solution_challenge', 'solution_user',
                          'solution_body', 'solution_created'], [c.get_name() for c in columns])
        self.assertTrue(columns[0].is_primary())
        self.assertFalse(columns[1].is_primary())
        self.assertFalse(columns[2].is_primary())

    def test_unsolved_and_started_attempt_are_denied(self):
        user = MagicMock()
        user.get_id.return_value = '5'
        challenge = MagicMock()
        challenge.get_id.return_value = '7'
        table = MagicMock()
        table.select.return_value.where.return_value.nocache.return_value.first.return_value.exec.return_value.fetch_object.return_value = None
        with patch('gdo.mira_challs.method.solutions.GDO_ChallengeSolved.table', return_value=table):
            self.assertFalse(solved_by(user, challenge))
        self.assertIn('solve_timestamp IS NOT NULL', table.select.return_value.where.call_args.args[0])

    def test_denied_request_does_not_render_or_submit(self):
        method = solutions.__new__(solutions)
        method._env_user = MagicMock()
        with patch.object(solutions, 'get_challenge', return_value=MagicMock()), \
             patch('gdo.mira_challs.method.solutions.solved_by', return_value=False), \
             patch.object(Application, 'IS_HTTP', True), \
             patch.object(Application, 'status') as status, \
             patch.object(solutions, 'err', return_value='denied'), \
             patch.object(MethodForm, 'gdo_execute') as execute, \
             patch.object(GDO_ChallengeSolution, 'blank') as blank:
            self.assertEqual('denied', method.gdo_execute())
            self.assertEqual('denied', method.form_submitted())
            execute.assert_not_called()
            blank.assert_not_called()
            self.assertEqual(2, status.call_count)

    def test_solver_can_submit_multiple_separate_records(self):
        method = solutions.__new__(solutions)
        method._env_user = MagicMock()
        method._env_user.get_id.return_value = '5'
        challenge = MagicMock()
        challenge.get_id.return_value = '7'
        form = MagicMock()
        form.get_field.return_value.get_val.return_value = 'My **solution**'
        with patch.object(solutions, 'get_challenge', return_value=challenge), \
             patch.object(solutions, 'get_form', return_value=form), \
             patch.object(solutions, 'param_val', return_value='BJ'), \
             patch.object(solutions, 'redirect_msg', return_value='saved'), \
             patch('gdo.mira_challs.method.solutions.href', return_value='/solutions/BJ'), \
             patch('gdo.mira_challs.method.solutions.solved_by', return_value=True), \
             patch.object(GDO_ChallengeSolution, 'blank') as blank:
            self.assertEqual('saved', method.form_submitted())
            self.assertEqual('saved', method.form_submitted())
            self.assertEqual(2, blank.return_value.insert.call_count)
            blank.assert_called_with({'solution_challenge': '7', 'solution_user': '5',
                                      'solution_body': 'My **solution**'})

    def test_solver_reads_only_requested_challenge_without_cache(self):
        method = solutions.__new__(solutions)
        method._env_user = MagicMock()
        challenge = MagicMock()
        challenge.get_id.return_value = '7'
        form = MagicMock()
        table = MagicMock()
        query = table.select.return_value.where.return_value.order.return_value.nocache.return_value
        query.exec.return_value = []
        with patch.object(solutions, 'get_challenge', return_value=challenge), \
             patch.object(solutions, 'get_form', return_value=form), \
             patch.object(MethodForm, 'gdo_execute', return_value=form), \
             patch.object(Application, 'get_mode', return_value=None), \
             patch.object(Application, 'IS_HTTP', True), \
             patch.object(Application, 'header') as header, \
             patch('gdo.mira_challs.method.solutions.solved_by', return_value=True), \
             patch.object(GDO_ChallengeSolution, 'table', return_value=table):
            method.gdo_execute()
            table.select.return_value.where.assert_called_once_with('solution_challenge=7')
            header.assert_any_call('Cache-Control', 'private, no-store')

    def test_markdown_editor_filters_script(self):
        result = MarkdownEditor.to_html('hello <script>alert(1)</script>')
        self.assertNotIn('<script', result.lower())
