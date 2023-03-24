from .base_repository import BaseRepository
from data.utils.constants import constants


class UsersRepository(BaseRepository):
    def find_by_username(self, username):
        pipeline = [
            {
                "$match": {
                    "username": username
                }
            }
        ]
        return self._find(pipeline)

    def get_page_by_role(self, role, page, page_size):
        pipeline = [{"$match": {"role": role}}]
        return self._get_page(pipeline, page, page_size)
