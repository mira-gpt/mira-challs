"""Opt-in test using connection-local temporary tables in the test database."""
import os
import unittest
from unittest.mock import patch


@unittest.skipUnless(os.environ.get('PYGDO_TAGS_DB_TEST') == '1', 'isolated database test is opt-in')
class ChallengeTagsDatabaseTest(unittest.TestCase):
    def test_challenges_share_and_remove_tags(self):
        from gdo.base.Application import Application
        from gdo.base.Render import Mode
        from gdo.mira_challs.GDO_Challenge import GDO_Challenge
        from gdo.mira_challs.GDO_ChallengeTag import GDO_ChallengeTag
        from gdo.mira_challs.GDO_ChallengeTagLink import GDO_ChallengeTagLink

        Application.init('/home/gizmore/www/pygdo', 'protected/pygdo_tes.toml')
        Application.mode(Mode.render_html)
        db = Application.db()
        self.assertEqual('pygdo_tes', db.db_name)
        db.query('CREATE TEMPORARY TABLE gdo_challenge (chall_id INT AUTO_INCREMENT PRIMARY KEY, chall_name VARCHAR(192) UNIQUE NOT NULL, chall_description VARCHAR(128), chall_score INT, chall_secret VARCHAR(255), chall_creator INT, chall_created DATETIME) ENGINE=InnoDB')
        db.query('CREATE TEMPORARY TABLE gdo_challengetag (tag_id INT AUTO_INCREMENT PRIMARY KEY, tag_name VARCHAR(64) UNIQUE NOT NULL, tag_created DATETIME, tag_creator INT) ENGINE=InnoDB')
        db.query('CREATE TEMPORARY TABLE gdo_challengetaglink (tag_id INT NOT NULL, obj_id INT NOT NULL, tag_created DATETIME, tag_creator INT, PRIMARY KEY (tag_id, obj_id)) ENGINE=InnoDB')
        with patch('gdo.core.GDT_Creator.GDT_Creator.gdo_before_create'), \
             patch.object(GDO_Challenge, 'gdo_cached', return_value=False), \
             patch.object(GDO_ChallengeTag, 'gdo_cached', return_value=False), \
             patch.object(GDO_ChallengeTagLink, 'gdo_cached', return_value=False):
            first = GDO_Challenge.blank({'chall_name': 'First'}).insert()
            second = GDO_Challenge.blank({'chall_name': 'Second'}).insert()
            with self.assertRaises(ValueError):
                first.add_tag('crypto')
            first.add_tag('crypto', allow_creation=True)
            first.add_tag('crypto')
            second.add_tag('crypto')
            self.assertEqual(['crypto'], [tag.gdo_val('tag_name') for tag in first.get_tags()])
            self.assertEqual(2, int(db.select('SELECT COUNT(*) FROM gdo_challengetaglink').fetch_val()))
            self.assertTrue(first.remove_tag('crypto'))
            self.assertFalse(first.remove_tag('crypto'))
            self.assertEqual(['crypto'], [tag.gdo_val('tag_name') for tag in second.get_tags()])
