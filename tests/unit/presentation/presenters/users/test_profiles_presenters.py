from mock import Mock

from presentation.presenters.users import (
    AdminProfilePresenter,
    CommunitySocialWorkerProfilePresenter,
    PublicOfficialProfilePresenter
)
from tests.factories.users import ProfilesFactory


class TestAdminProfilePresenter():
    def setup_method(self):
        self.presenter = AdminProfilePresenter()

    def test_present(self):
        admin_profile = ProfilesFactory.admin()
        principal_mock = Mock()

        result = self.presenter.present(admin_profile, principal_mock)

        assert result == {
            "first_name": admin_profile.first_name,
            "last_name": admin_profile.last_name
        }


class TestCommunitySocialWorkerProfilePresenter():
    def setup_method(self):
        self.presenter = CommunitySocialWorkerProfilePresenter()

    def test_present(self):
        community_social_worker_profile = ProfilesFactory.community_social_worker()
        principal_mock = Mock()

        result = self.presenter.present(
            community_social_worker_profile,
            principal_mock
        )

        assert result == {
            "first_name": community_social_worker_profile.first_name,
            "last_name": community_social_worker_profile.last_name
        }


class TestPublicOfficialProfilePresenter():
    def setup_method(self):
        self.presenter = PublicOfficialProfilePresenter()

    def test_present(self):
        public_official_profile = ProfilesFactory.public_official()
        principal_mock = Mock()

        result = self.presenter.present(public_official_profile, principal_mock)

        assert result == {
            "first_name": public_official_profile.first_name,
            "last_name": public_official_profile.last_name
        }
