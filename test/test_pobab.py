import unittest
from unittest.mock import MagicMock, patch

from gdo.base.Application import Application
from gdo.mira_challs.challs.POBAB.POBAB import POBAB, solution, starting_values


class POBABTest(unittest.TestCase):
    def test_solution_and_strict_answer_format(self):
        self.assertEqual('4360633075607906', starting_values(42))
        self.assertEqual('3350779673064306', solution(42))
        puzzle = POBAB()
        user = MagicMock()
        user.get_id.return_value = '42'
        self.assertTrue(puzzle.check_answer_for_user('3350779673064306', user))
        self.assertTrue(puzzle.check_answer_for_user(' 3350779673064306 ', user))
        for answer in (None, '', '3350779673064307', '3350 7796 7306 4306', '33507796730643060'):
            with self.subTest(answer=answer):
                self.assertFalse(puzzle.check_answer_for_user(answer, user))

    def test_user_ids_are_stable_and_independent(self):
        self.assertEqual(starting_values('42'), starting_values(42))
        self.assertNotEqual(starting_values(42), starting_values(43))
        self.assertNotEqual(solution(42), solution(43))
        user = MagicMock()
        user.get_id.return_value = '43'
        self.assertFalse(POBAB().check_answer_for_user(solution(42), user))
        self.assertTrue(POBAB().check_answer_for_user(solution(43), user))
        with self.assertRaises(ValueError):
            starting_values('not-a-user-id')

    def test_page_has_puzzle_and_answer_box(self):
        method = MagicMock()
        method._env_user.get_name.return_value = '<visitor>'
        method._env_user.get_id.return_value = '42'
        method.t.side_effect = lambda key, args: f'{key}: {args[0]}'
        with patch.object(Application, 'get_mode', return_value=None), \
                patch('gdo.mira_challs.challs.POBAB.POBAB.GDT_AnswerBox') as answer:
            POBAB.challenge_page(method)
            answer.assert_called_once_with(challenge_name='POBAB')
            self.assertEqual('&lt;visitor&gt;', method.t.call_args.args[1][0])
            self.assertIn('A=4', method.t.call_args.args[1][1])
