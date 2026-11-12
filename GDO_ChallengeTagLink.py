from gdo.tags.GDO_TagObject import GDO_TagObject


class GDO_ChallengeTagLink(GDO_TagObject):
    def gdo_tags_table(self):
        from gdo.mira_challs.GDO_ChallengeTag import GDO_ChallengeTag
        return GDO_ChallengeTag.table()

    def gdo_tag_object_table(self):
        from gdo.mira_challs.GDO_Challenge import GDO_Challenge
        return GDO_Challenge.table()
