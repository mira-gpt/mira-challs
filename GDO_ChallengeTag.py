from gdo.tags.GDO_Tag import GDO_Tag


class GDO_ChallengeTag(GDO_Tag):
    def gdo_tag_object_table(self):
        from gdo.mira_challs.GDO_ChallengeTagLink import GDO_ChallengeTagLink
        return GDO_ChallengeTagLink.table()
