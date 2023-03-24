from mock import Mock

from domain.entities.polls.requests import GetPollsPageRequest


class TestGetPollsPageRequest():
    def setup_method(self):
        self.principal_mock = Mock()
        self.user_id = "test_user_id"
        self.page = 1
        self.page_size = 10

        self.entity = GetPollsPageRequest(
            self.principal_mock,
            self.user_id,
            self.page,
            self.page_size
        )

    def test_init(self):
        assert self.entity.principal == self.principal_mock
        assert self.entity.user_id == self.user_id
        assert self.entity.page == self.page
        assert self.entity.page_size == self.page_size
