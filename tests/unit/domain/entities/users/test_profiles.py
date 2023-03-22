from mock import Mock

from domain.entities.users import (
    AdminProfile,
    CommunitySocialWorkerProfile,
    PublicOfficialProfile
)


class TestAdminProfile():
    def setup_method(self):
        self.first_name = "test_first_name"
        self.last_name = "test_last_name"

        self.entity = AdminProfile(self.first_name, self.last_name)

    def test_init(self):
        assert self.entity.first_name == self.first_name
        assert self.entity.last_name == self.last_name


class TestCommunitySocialWorkerProfile():
    def setup_method(self):
        self.first_name = "test_first_name"
        self.last_name = "test_last_name"

        self.entity = CommunitySocialWorkerProfile(
            self.first_name,
            self.last_name
        )

    def test_init(self):
        assert self.entity.first_name == self.first_name
        assert self.entity.last_name == self.last_name

    def test_from_create_user_request(self):
        create_user_request_mock = Mock()
        create_user_request_mock.first_name = "test_first_name"
        create_user_request_mock.last_name = "test_last_name"

        result = CommunitySocialWorkerProfile.from_create_user_request(
            create_user_request_mock
        )

        assert isinstance(result, CommunitySocialWorkerProfile) is True
        assert result.first_name == create_user_request_mock.first_name
        assert result.last_name == create_user_request_mock.last_name


class TestPublicOfficialProfile():
    def setup_method(self):
        self.first_name = "test_first_name"
        self.last_name = "test_last_name"

        self.entity = PublicOfficialProfile(self.first_name, self.last_name)

    def test_init(self):
        assert self.entity.first_name == self.first_name
        assert self.entity.last_name == self.last_name

    def test_from_create_user_request(self):
        create_user_request_mock = Mock()
        create_user_request_mock.first_name = "test_first_name"
        create_user_request_mock.last_name = "test_last_name"

        result = PublicOfficialProfile.from_create_user_request(
            create_user_request_mock
        )

        assert isinstance(result, PublicOfficialProfile) is True
        assert result.first_name == create_user_request_mock.first_name
        assert result.last_name == create_user_request_mock.last_name
