from mock import Mock

from domain.entities.polls.requests import GetPollsSummaryRequest


class TestGetPollsSummaryRequest():
    def setup_method(self):
        self.principal_mock = Mock()

        self.entity = GetPollsSummaryRequest(self.principal_mock)

    def test_init(self):
        assert self.entity.principal == self.principal_mock
