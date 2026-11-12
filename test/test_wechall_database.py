"""Optional integration test; all tables are connection-local and temporary."""
import os
import unittest


@unittest.skipUnless(os.environ.get('PYGDO_WECHALL_DB_TEST') == '1', 'isolated database test is opt-in')
class WeChallDatabaseTest(unittest.TestCase):
    def test_exact_qualified_account_lookup(self):
        from gdo.base.Application import Application
        from gdo.mira_challs.WeChallAPI import resolve_onsite_user

        Application.init('/home/gizmore/www/pygdo', 'protected/pygdo_tes.toml')
        db = Application.db()
        self.assertEqual('pygdo_tes', db.db_name)
        db.query('CREATE TEMPORARY TABLE gdo_server (serv_id INT PRIMARY KEY, serv_name VARCHAR(100))')
        db.query('CREATE TEMPORARY TABLE gdo_user (user_id INT PRIMARY KEY, user_name VARCHAR(100), user_displayname VARCHAR(100), user_server INT, user_type VARCHAR(20), user_link INT NULL)')
        try:
            db.query("INSERT INTO gdo_server VALUES (90001, 'Web'), (90002, 'Discord')")
            db.query("INSERT INTO gdo_user VALUES (90001, 'Example', 'Example', 90001, 'member', NULL), (90002, 'Example', 'Example', 90002, 'member', NULL)")
            self.assertEqual('90001', str(resolve_onsite_user('Example{web}').get_id()))
            self.assertEqual('90002', str(resolve_onsite_user('Example{discord}').get_id()))
            self.assertIsNone(resolve_onsite_user('example{web}'))
            self.assertIsNone(resolve_onsite_user('Example'))
            db.query("INSERT INTO gdo_user VALUES (90003, 'Example', 'Example', 90001, 'member', NULL)")
            self.assertIsNone(resolve_onsite_user('Example{web}'))
        finally:
            db.get_link().close()
            db.link = None
