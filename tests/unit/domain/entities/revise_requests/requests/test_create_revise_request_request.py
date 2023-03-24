from mock import Mock

from domain.entities.revise_requests.requests import CreateReviseRequestRequest


class TestCreateReviseRequestRequest():
    def setup_method(self):
        self.principal_mock = Mock()
        self.poll_id = "test_poll_id"

        self.entity = CreateReviseRequestRequest(
            self.principal_mock,
            self.poll_id
        )

    def test_init(self):
        assert self.entity.principal == self.principal_mock
        assert self.entity.poll_id == self.poll_id
