from mock import Mock

from domain.utils import constants
from presentation.presenters.users import UserPresenter
from tests.factories.users import UserFactory


class TestUserPresenter():
    def setup_method(self):
        self.admin_profile_presenter_mock = Mock()
        self.profile_presenters = {
            constants.user_roles.admin: self.admin_profile_presenter_mock
        }

        self.presenter = UserPresenter(self.profile_presenters)

    def test_init(self):
        assert self.presenter.profile_presenters == self.profile_presenters

    def test_present(self):
        presented_profile_mock = Mock()
        self.admin_profile_presenter_mock.present.return_value =\
            presented_profile_mock

        user = UserFactory.admin()
        principal_mock = Mock()

        result = self.presenter.present(user, principal_mock)

        assert result == {
            "id": user.id,
            "role": user.role,
            "username": user.username,
            "profile": presented_profile_mock
        }
        self.admin_profile_presenter_mock.present.assert_called_once_with(
            user.profile,
            principal_mock
        )
