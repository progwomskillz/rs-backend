from mock import Mock

from presentation.presenters.polls import StatsPresenter
from tests.factories.polls import StatsFactory


class TestStatsPresenter():
    def setup_method(self):
        self.presenter = StatsPresenter()

    def test_present(self):
        stats = StatsFactory.generic()
        principal_mock = Mock()

        result = self.presenter.present(stats, principal_mock)

        assert result == {
            "title": stats.title,
            "count": stats.count,
            "percentage": stats.percentage
        }
