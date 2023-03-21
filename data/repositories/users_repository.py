import re

from .base_repository import BaseRepository


class UsersRepository(BaseRepository):
    def find_by_email(self, email):
        pipeline = [
            {
                "$match": {
                    "email": {
                        "$regex": f"^{re.escape(email)}$",
                        "$options": "i"
                    }
                }
            }
        ]
        return self._find(pipeline)

    def get_page_by_role(self, role, page, page_size):
        pipeline = [{"$match": {"role": role}}]
        return self._get_page(pipeline, page, page_size)
