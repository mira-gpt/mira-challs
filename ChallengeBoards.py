from gdo.base.Application import Application
from gdo.forum.GDO_ForumBoard import GDO_ForumBoard


class ChallengeBoards:
    """Create missing challenge boards without changing existing boards."""

    @staticmethod
    def find_board(name):
        table = GDO_ForumBoard.table()
        return (table.select().where(f'board_name={table.quote(name)}')
                .nocache().first().exec().fetch_object())

    @classmethod
    def ensure(cls, challenges):
        db = Application.db()
        owns_transaction = not db.is_in_transaction()
        if owns_transaction:
            db.begin()
        try:
            # Serialize the lookup and nested-set updates with other creators.
            GDO_ForumBoard.lock_tree()
            parent = cls.find_board('Mira-Challs')
            if not parent:
                root = GDO_ForumBoard.table().get_by_aid('1')
                if not root:
                    raise ValueError('Forum root is missing; install the forum first.')
                parent = GDO_ForumBoard.create_child(root, 'Mira Challenges', name='Mira-Challs')
            for challenge in challenges:
                name = challenge.gdo_val('chall_name')
                board = cls.find_board(name)
                if board:
                    actual_parent = board.parent()
                    if not actual_parent or actual_parent.get_id() != parent.get_id():
                        raise ValueError(f'Forum board {name} already exists outside Mira-Challs.')
                else:
                    GDO_ForumBoard.create_child(parent, name, name=name)
            if owns_transaction:
                db.commit()
        except Exception:
            if owns_transaction:
                db.rollback()
            raise
