from .base_repository import BaseRepository
from data.utils import constants


class ReviseRequestsRepository(BaseRepository):
    def __init__(
        self, scheme, username, password, host, port, db_name, collection_name,
        translator
    ):
        super().__init__(
            scheme, username, password, host, port, db_name, collection_name,
            translator, constants.pipelines.revise_requests.default
        )
