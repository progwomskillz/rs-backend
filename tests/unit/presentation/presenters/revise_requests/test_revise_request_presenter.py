from mock import Mock

from domain.utils import constants
from presentation.presenters.revise_requests import ReviseRequestPresenter
from tests.factories.revise_requests import ReviseRequestFactory


class TestUserPresenter():
    def setup_method(self):
        self.poll_presenter_mock = Mock()

        self.presenter = ReviseRequestPresenter(self.poll_presenter_mock)

    def test_init(self):
        assert self.presenter.poll_presenter == self.poll_presenter_mock

    def test_present(self):
        presented_poll_mock = Mock()
        self.poll_presenter_mock.present.return_value = presented_poll_mock

        revise_request = ReviseRequestFactory.generic()
        principal_mock = Mock()

        result = self.presenter.present(revise_request, principal_mock)

        assert result == {
            "id": revise_request.id,
            "poll": presented_poll_mock
        }
        self.poll_presenter_mock.present.assert_called_once_with(
            revise_request.poll,
            principal_mock
        )
