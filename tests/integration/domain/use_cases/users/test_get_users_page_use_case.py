import pytest

from application.structure import structure
from data.repositories.mongo import MongoUsersRepository
from domain.entities.auth import Principal, TokensPayload
from domain.entities.exceptions import (
    UnauthenticatedException,
    UnauthorizedException,
    InvalidRequest
)
from domain.entities.shared import Page
from domain.entities.users.requests import GetUsersPageRequest
from domain.entities.users import User
from domain.utils.validation.users import GetUsersPageRequestValidationUtil
from domain.utils.validation import PrincipalValidationUtil, RBACValidationUtil
from domain.utils import constants
from tests.factories.users import UserFactory


class TestGetUsersPageUseCase():
    def setup_method(self):
        self.use_case = structure.get_users_page_use_case

        self.users_repository = structure.mongo_users_repository

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
            self.use_case.get_users_page_request_validation_util,
            GetUsersPageRequestValidationUtil
        ) is True
        assert isinstance(
            self.use_case.users_repository,
            MongoUsersRepository
        ) is True

    def test_get_users_page_invalid_principal(self):
        principal = None
        role = None
        page = None
        page_size = None
        get_users_page_request = GetUsersPageRequest(
            principal,
            role,
            page,
            page_size
        )

        with pytest.raises(UnauthenticatedException):
            self.use_case.get_users_page(get_users_page_request)

    def test_get_users_page_invalid_principal_role(self):
        user = UserFactory.community_social_worker()
        principal = Principal(user, None)
        role = None
        page = None
        page_size = None
        get_users_page_request = GetUsersPageRequest(
            principal,
            role,
            page,
            page_size
        )

        with pytest.raises(UnauthorizedException):
            self.use_case.get_users_page(get_users_page_request)

    def test_get_users_page_invalid_request(self):
        def assert_getting(user, available_roles):
            user_id = self.users_repository.create(user)
            user.on_create(user_id)
            tokens_payload = TokensPayload(user.id, user.role)
            tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
            user.on_login(tokens_pair)
            self.users_repository.update(user)

            principal = Principal(user, tokens_pair)
            role = None
            page = None
            page_size = None
            get_users_page_request = GetUsersPageRequest(
                principal,
                role,
                page,
                page_size
            )

            with pytest.raises(InvalidRequest) as e:
                self.use_case.get_users_page(get_users_page_request)

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
                        "message": f"Must be in \"{available_roles}\"",
                        "code": "entry"
                    }
                ],
                "page": [
                    {
                        "message": "Has to be present",
                        "code": "presence"
                    },
                    {
                        "message": "Must be of type \"integer\"",
                        "code": "type"
                    }
                ],
                "page_size": [
                    {
                        "message": "Has to be present",
                        "code": "presence"
                    },
                    {
                        "message": "Must be of type \"integer\"",
                        "code": "type"
                    }
                ]
            }

        assert_getting(
            UserFactory.admin(),
            [
                constants.user_roles.community_social_worker,
                constants.user_roles.public_official
            ]
        )
        assert_getting(
            UserFactory.public_official(),
            [constants.user_roles.community_social_worker]
        )

    def test_get_users_page(self):
        user = UserFactory.admin()
        user_id = self.users_repository.create(user)
        user.on_create(user_id)
        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
        user.on_login(tokens_pair)
        self.users_repository.update(user)

        principal = Principal(user, tokens_pair)

        role = constants.user_roles.public_official
        page = 1
        page_size = 10
        get_users_page_request = GetUsersPageRequest(
            principal,
            role,
            page,
            page_size
        )

        for _ in range(page * page_size + 1):
            self.users_repository.create(UserFactory.public_official())

        result = self.use_case.get_users_page(get_users_page_request)

        assert isinstance(result, Page) is True
        assert len(result.items) == page_size
        assert result.page == page
        assert result.page_count == page + 1
        for item in result.items:
            assert isinstance(item, User) is True
            assert item.role == constants.user_roles.public_official
