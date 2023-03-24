from mock import Mock

from domain.entities.revise_requests.requests import GetReviseRequestsPageRequest


class TestGetReviseRequestsPageRequest():
    def setup_method(self):
        self.principal_mock = Mock()
        self.page = 1
        self.page_size = 10

        self.entity = GetReviseRequestsPageRequest(
            self.principal_mock,
            self.page,
            self.page_size
        )

    def test_init(self):
        assert self.entity.principal == self.principal_mock
        assert self.entity.page == self.page
        assert self.entity.page_size == self.page_size
