import unittest
from unittest.mock import MagicMock, patch

from gdo.mira_challs.ChallengeBoards import ChallengeBoards
from gdo.mira_challs.module_mira_challs import module_mira_challs


class ChallengeBoardsTest(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock()
        self.db.is_in_transaction.return_value = False
        self.parent = MagicMock()
        self.parent.get_id.return_value = '2'
        self.challenge = MagicMock()
        self.challenge.gdo_val.return_value = 'BJ'

    def test_forum_is_a_dependency(self):
        self.assertIn('forum', module_mira_challs().gdo_dependencies())

    def test_creates_exact_name_beneath_existing_parent(self):
        with patch('gdo.mira_challs.ChallengeBoards.Application.db', return_value=self.db), \
             patch('gdo.mira_challs.ChallengeBoards.GDO_ForumBoard.lock_tree') as lock, \
             patch.object(ChallengeBoards, 'find_board', side_effect=[self.parent, None]), \
             patch('gdo.mira_challs.ChallengeBoards.GDO_ForumBoard.create_child') as create:
            ChallengeBoards.ensure([self.challenge])
        lock.assert_called_once()
        create.assert_called_once_with(self.parent, 'BJ', name='BJ')
        self.db.commit.assert_called_once()

    def test_existing_board_is_not_duplicated(self):
        child = MagicMock()
        child.parent.return_value = self.parent
        with patch('gdo.mira_challs.ChallengeBoards.Application.db', return_value=self.db), \
             patch('gdo.mira_challs.ChallengeBoards.GDO_ForumBoard.lock_tree'), \
             patch.object(ChallengeBoards, 'find_board', side_effect=[self.parent, child]), \
             patch('gdo.mira_challs.ChallengeBoards.GDO_ForumBoard.create_child') as create:
            ChallengeBoards.ensure([self.challenge])
        create.assert_not_called()

    def test_existing_board_under_other_parent_aborts(self):
        child = MagicMock()
        child.parent.return_value.get_id.return_value = '99'
        with patch('gdo.mira_challs.ChallengeBoards.Application.db', return_value=self.db), \
             patch('gdo.mira_challs.ChallengeBoards.GDO_ForumBoard.lock_tree'), \
             patch.object(ChallengeBoards, 'find_board', side_effect=[self.parent, child]), \
             patch('gdo.mira_challs.ChallengeBoards.GDO_ForumBoard.create_child') as create:
            with self.assertRaises(ValueError):
                ChallengeBoards.ensure([self.challenge])
        create.assert_not_called()
        self.db.rollback.assert_called_once()

    def test_missing_parent_is_created_beneath_forum_root(self):
        root = MagicMock()
        with patch('gdo.mira_challs.ChallengeBoards.Application.db', return_value=self.db), \
             patch('gdo.mira_challs.ChallengeBoards.GDO_ForumBoard.lock_tree'), \
             patch.object(ChallengeBoards, 'find_board', side_effect=[None, None]), \
             patch('gdo.mira_challs.ChallengeBoards.GDO_ForumBoard.table') as table, \
             patch('gdo.mira_challs.ChallengeBoards.GDO_ForumBoard.create_child', return_value=self.parent) as create:
            table.return_value.get_by_aid.return_value = root
            ChallengeBoards.ensure([self.challenge])
        self.assertEqual(('Mira Challenges',), create.call_args_list[0].args[1:])
        self.assertEqual({'name': 'Mira-Challs'}, create.call_args_list[0].kwargs)
        self.assertEqual((self.parent, 'BJ'), create.call_args_list[1].args)

    def test_existing_transaction_is_owned_by_caller(self):
        self.db.is_in_transaction.return_value = True
        with patch('gdo.mira_challs.ChallengeBoards.Application.db', return_value=self.db), \
             patch('gdo.mira_challs.ChallengeBoards.GDO_ForumBoard.lock_tree'), \
             patch.object(ChallengeBoards, 'find_board', side_effect=[self.parent, None]), \
             patch('gdo.mira_challs.ChallengeBoards.GDO_ForumBoard.create_child'):
            ChallengeBoards.ensure([self.challenge])
        self.db.begin.assert_not_called()
        self.db.commit.assert_not_called()
        self.db.rollback.assert_not_called()
