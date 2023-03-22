import pytest

from application.structure import structure
from data.repositories import UsersRepository
from data.utils.wrappers import BcryptWrapper
from domain.entities.auth import TokensPayload, Principal
from domain.entities.exceptions import (
    UnauthenticatedException,
    UnauthorizedException,
    InvalidRequest
)
from domain.entities.users.requests import CreateUserRequest
from domain.entities.users import (
    CommunitySocialWorkerProfile,
    PublicOfficialProfile,
    User
)
from domain.utils.validation import PrincipalValidationUtil, RBACValidationUtil
from domain.utils.validation.users import CreateUserRequestValidationUtil
from domain.utils import constants
from tests.factories.users import UserFactory


class TestCreateUserUseCase():
    def setup_method(self):
        self.use_case = structure.create_user_use_case

        self.users_repository = structure.users_repository

    def teardown_method(self):
        self.users_repository.collection.delete_many({})

    def test_init(self):
        assert isinstance(
            self.use_case.principal_validation_util,
            PrincipalValidationUtil
        ) is True
        assert isinstance(
            self.use_case.rbac_validation_util,
            RBACValidationUtil
        ) is True
        assert isinstance(
            self.use_case.create_user_request_validation_util,
            CreateUserRequestValidationUtil
        ) is True
        assert isinstance(self.use_case.password_util, BcryptWrapper) is True
        assert isinstance(
            self.use_case.users_repository,
            UsersRepository
        ) is True

    def test_create_user_invalid_principal(self):
        principal = None
        role = None
        email = None
        password = None
        first_name = None
        last_name = None
        create_user_request = CreateUserRequest(
            principal,
            role,
            email,
            password,
            first_name,
            last_name
        )

        with pytest.raises(UnauthenticatedException):
            self.use_case.create_user(create_user_request)

    def test_create_user_invalid_principal_role(self):
        def assert_creating(user):
            principal = Principal(user, None)
            role = None
            email = None
            password = None
            first_name = None
            last_name = None
            create_user_request = CreateUserRequest(
                principal,
                role,
                email,
                password,
                first_name,
                last_name
            )

            with pytest.raises(UnauthorizedException):
                self.use_case.create_user(create_user_request)
        
        assert_creating(UserFactory.community_social_worker())
        assert_creating(UserFactory.public_official())

    def test_create_user_invalid_request(self):
        user = UserFactory.admin()
        user_id = self.users_repository.create(user)
        user.on_create(user_id)
        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
        user.on_login(tokens_pair)
        self.users_repository.update(user)

        principal = Principal(user, tokens_pair)
        role = None
        email = None
        password = None
        first_name = None
        last_name = None
        create_user_request = CreateUserRequest(
            principal,
            role,
            email,
            password,
            first_name,
            last_name
        )

        with pytest.raises(InvalidRequest) as e:
            self.use_case.create_user(create_user_request)

        assert e.value.errors == {
            "role": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"string\"",
                    "code": "type"
                },
                {
                    "message": f"Must be in \"{[constants.user_roles.community_social_worker, constants.user_roles.public_official]}\"",
                    "code": "entry"
                }
            ],
            "email": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"string\"",
                    "code": "type"
                },
                {
                    "message": "Must be \"*@*\" format without any whitespaces",
                    "code": "email_format"
                },
                {
                    "message": "Must be unique",
                    "code": "unique"
                }
            ],
            "password": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"string\"",
                    "code": "type"
                }
            ],
            "first_name": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"string\"",
                    "code": "type"
                }
            ],
            "last_name": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"string\"",
                    "code": "type"
                }
            ]
        }

    def test_create_user(self):
        user = UserFactory.admin()
        user_id = self.users_repository.create(user)
        user.on_create(user_id)
        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
        user.on_login(tokens_pair)
        self.users_repository.update(user)

        principal = Principal(user, tokens_pair)

        profiles_classes = {
            constants.user_roles.community_social_worker: CommunitySocialWorkerProfile,
            constants.user_roles.public_official: PublicOfficialProfile
        }

        def assert_creating(role):
            email = f"test_{role}@example.com"
            password = "test_password"
            first_name = "test_first_name"
            last_name = "test_last_name"
            create_user_request = CreateUserRequest(
                principal,
                role,
                email,
                password,
                first_name,
                last_name
            )

            result = self.use_case.create_user(create_user_request)

            assert isinstance(result, User) is True
            assert result.email == email
            assert structure.bcrypt_wrapper.compare(password, result.password_hash)
            assert isinstance(result.profile, profiles_classes[role]) is True
            assert result.profile.first_name == first_name
            assert result.profile.last_name == last_name

            result_user = self.users_repository.find_by_id(result.id)
            assert isinstance(result_user, User) is True

        assert_creating(constants.user_roles.community_social_worker)
        assert_creating(constants.user_roles.public_official)
