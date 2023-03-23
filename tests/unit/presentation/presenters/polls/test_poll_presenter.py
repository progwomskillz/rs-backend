from mock import Mock

from presentation.presenters.polls import PollPresenter
from tests.factories.polls import PollFactory
from tests.factories.users import UserFactory


class TestPollPresenter():
    def setup_method(self):
        self.user_presenter_mock = Mock()
        self.stats_presenter_mock = Mock()

        self.presenter = PollPresenter(
            self.user_presenter_mock,
            self.stats_presenter_mock
        )

    def test_init(self):
        assert self.presenter.user_presenter == self.user_presenter_mock
        assert self.presenter.stats_presenter == self.stats_presenter_mock

    def test_present(self):
        presented_user_mock = Mock()
        self.user_presenter_mock.present.return_value = presented_user_mock
        presented_stats_mock = Mock()
        self.stats_presenter_mock.present.return_value = presented_stats_mock

        poll = PollFactory.generic()
        principal_mock = Mock()

        result = self.presenter.present(poll, principal_mock)

        assert result == {
            "id": poll.id,
            "user": presented_user_mock,
            "community_name": poll.community_name,
            "community_size": poll.community_size,
            "summary": [
                presented_stats_mock
                for _ in range(len(poll.summary))
            ]
        }
        self.user_presenter_mock.present.assert_called_once_with(
            poll.user,
            principal_mock
        )
        assert self.stats_presenter_mock.present.call_count == len(poll.summary)
        for stats in poll.summary:
            self.stats_presenter_mock.present.assert_any_call(
                stats,
                principal_mock
            )
