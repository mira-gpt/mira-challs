"""Backfill declared tags for challenges installed before tagging existed."""

from gdo.mira_challs.GDO_Challenge import GDO_Challenge
from gdo.tags.GDT_Tags import GDT_Tags


def sync_declared_tags(records):
    """Add missing declared tags only; never remove existing associations."""
    for record in records:
        challenge = GDO_Challenge.load_challenge(record.gdo_val('chall_name'))
        for tag in GDT_Tags.parse_names(challenge.get_challenge_tags()):
            record.add_tag(tag, allow_creation=True)
