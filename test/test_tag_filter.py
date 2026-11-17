import unittest
from unittest.mock import MagicMock, patch

from gdo.mira_challs.method.challenges import challenges


class ChallengeTagFilterTest(unittest.TestCase):
    def test_cloud_uses_tag_counts_and_translation(self):
        method = challenges.__new__(challenges)
        tags, links = MagicMock(), MagicMock()
        tags.gdo_table_name.return_value = 'gdo_challengetag'
        links.gdo_table_name.return_value = 'gdo_challengetaglink'
        tags.select.return_value.join.return_value.group.return_value.order.return_value.exec.return_value.iter.return_value = [(4, 'crypto', 2)]
        with patch('gdo.mira_challs.method.challenges.GDO_ChallengeTag.table', return_value=tags), \
             patch('gdo.mira_challs.method.challenges.GDO_ChallengeTagLink.table', return_value=links), \
             patch('gdo.mira_challs.method.challenges.href', side_effect=lambda *args, **kwargs: '/challenges'), \
             patch.object(challenges, 'param_value', return_value=4), \
             patch.object(challenges, 't', return_value='All challenges') as translate:
            html = method.tag_cloud().render_html()
        self.assertIn('crypto (2)', html)
        self.assertIn('aria-current="true"', html)
        translate.assert_called_once_with('mira_challs_all_tags', ())

    def test_backfill_adds_only_declared_tags(self):
        from gdo.mira_challs.ChallengeTags import sync_declared_tags
        record = MagicMock()
        record.gdo_val.return_value = 'Example'
        with patch('gdo.mira_challs.ChallengeTags.GDO_Challenge.load_challenge') as load:
            load.return_value.get_challenge_tags.return_value = 'challenge,crypto,challenge'
            sync_declared_tags([record])
        self.assertEqual(['challenge', 'crypto'], [call.args[0] for call in record.add_tag.call_args_list])
        record.remove_tag.assert_not_called()

    def test_query_filters_on_tag_without_duplicate_challenges(self):
        method = challenges.__new__(challenges)
        table = MagicMock()
        table.gdo_table_name.return_value = 'gdo_challenge'
        query = table.select.return_value
        query.nocache.return_value = query
        with patch.object(challenges, 'gdo_table', return_value=table), \
             patch.object(challenges, 'param_value', return_value=7):
            self.assertIs(query, method.gdo_table_query())
        query.where.assert_called_once_with(
            'gdo_challenge.chall_id IN (SELECT obj_id FROM gdo_challengetaglink WHERE tag_id = 7)')

    def test_unfiltered_query(self):
        method = challenges.__new__(challenges)
        table = MagicMock()
        query = table.select.return_value
        query.nocache.return_value = query
        with patch.object(challenges, 'gdo_table', return_value=table), \
             patch.object(challenges, 'param_value', return_value=None):
            method.gdo_table_query()
        query.where.assert_not_called()


if __name__ == '__main__':
    unittest.main()
