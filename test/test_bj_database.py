"""Opt-in integration check using only connection-local temporary test tables."""
import os
import unittest
from unittest.mock import MagicMock, patch


@unittest.skipUnless(os.environ.get('PYGDO_BJ_DB_TEST') == '1', 'isolated database test is opt-in')
class BJDatabaseTest(unittest.TestCase):
    def test_signed_answer_records_one_solve(self):
        from gdo.base.Application import Application
        from gdo.base.Render import Mode
        from gdo.core.ChallengeToken import issue
        from gdo.mira_challs.GDO_Challenge import GDO_Challenge
        from gdo.mira_challs.GDO_ChallengeSolved import GDO_ChallengeSolved
        from gdo.mira_challs.challs.BJ.BJ import BJ
        from gdo.mira_challs.method.solve import solve

        Application.init('/home/gizmore/www/pygdo', 'protected/pygdo_tes.toml')
        Application.mode(Mode.render_html)
        db = Application.db()
        self.assertEqual('pygdo_tes', db.db_name)
        db.query('CREATE TEMPORARY TABLE gdo_challenge (chall_id INT AUTO_INCREMENT PRIMARY KEY, chall_name VARCHAR(192) UNIQUE NOT NULL, chall_score INT, chall_secret VARCHAR(255), chall_creator INT, chall_created DATETIME) ENGINE=InnoDB')
        db.query('CREATE TEMPORARY TABLE gdo_challengesolved (solve_challenge INT NOT NULL, solve_user INT NOT NULL, solve_timestamp DATETIME, solve_created DATETIME NOT NULL, PRIMARY KEY (solve_challenge, solve_user)) ENGINE=InnoDB')
        db.begin()
        try:
            user = MagicMock()
            user.is_member.return_value = True
            user.get_id.return_value = '900001'
            key = b'k' * 32
            token = issue(key, 'bj1', 'synthetic player')
            with patch('gdo.core.GDT_Creator.GDT_Creator.gdo_before_create'), \
                 patch.object(GDO_Challenge, 'gdo_cached', return_value=False), \
                 patch.object(GDO_ChallengeSolved, 'gdo_cached', return_value=False), \
                 patch('gdo.mira_challs.challs.BJ.BJ.read_secret', return_value=key):
                GDO_Challenge.blank({'chall_name': 'BJ'}).insert()
                method = solve()
                method._env_user = user
                method.param_val = MagicMock(return_value='BJ')
                form = MagicMock()
                method.get_form = MagicMock(return_value=form)
                method.msg = MagicMock(side_effect=lambda key: key)
                method.err = MagicMock(side_effect=lambda key: key)
                form.get_field.return_value.get_val.return_value = 'invalid'
                self.assertEqual('err_mira_challs_wrong_answer', method.form_submitted())
                form.get_field.return_value.get_val.return_value = token
                self.assertEqual('msg_mira_challs_answer_correct', method.form_submitted())
                self.assertEqual('msg_mira_challs_already_solved', method.form_submitted())
                row = db.select('SELECT COUNT(*) AS n FROM gdo_challengesolved WHERE solve_timestamp IS NOT NULL').fetch_assoc()
                self.assertEqual(1, int(row['n']))
                with patch.object(Application, 'IS_HTTP', True), \
                     patch('gdo.form.GDT_CSRF.GDT_CSRF.generate_token', return_value='synthetic'):
                    page_method = MagicMock()
                    page_method.t.return_value = 'Instructions'
                    html = BJ.challenge_page(page_method).render_html()
                    self.assertIn('name="answer"', html)
                    self.assertIn('name="csrf"', html)
                    self.assertIn('mira_challs.solve.named.BJ.html', html)
                    self.assertIn('blackjack.site.html', html)
        finally:
            db.rollback()
            db.get_link().close()  # Closing removes both temporary tables.
            db.link = None
