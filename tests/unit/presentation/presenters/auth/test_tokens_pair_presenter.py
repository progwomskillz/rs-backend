from mock import Mock

from presentation.presenters.auth import TokensPairPresenter
from tests.factories.auth import TokensPairFactory


class TestTokensPairPresenter():
    def setup_method(self):
        self.presenter = TokensPairPresenter()

    def test_present(self):
        tokens_pair = TokensPairFactory.generic()
        principal_mock = Mock()

        result = self.presenter.present(tokens_pair, principal_mock)

        assert result == {
            "access": tokens_pair.access,
            "refresh": tokens_pair.refresh
        }
