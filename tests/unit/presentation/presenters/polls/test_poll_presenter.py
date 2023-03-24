from mock import Mock

from presentation.presenters.polls import PollPresenter
from tests.factories.polls import PollFactory
from tests.factories.users import UserFactory


class TestPollPresenter():
    def setup_method(self):
        self.stats_list_presenter_mock = Mock()

        self.presenter = PollPresenter(self.stats_list_presenter_mock)

    def test_init(self):
        assert self.presenter.stats_list_presenter ==\
            self.stats_list_presenter_mock

    def test_present(self):
        presented_summary_mock = Mock()
        self.stats_list_presenter_mock.present.return_value =\
            presented_summary_mock

        poll = PollFactory.generic()
        principal_mock = Mock()

        result = self.presenter.present(poll, principal_mock)

        assert result == {
            "id": poll.id,
            "community_name": poll.community_name,
            "community_size": poll.community_size,
            "summary": presented_summary_mock
        }
        self.stats_list_presenter_mock.present.assert_called_once_with(
            poll.summary,
            principal_mock
        )
