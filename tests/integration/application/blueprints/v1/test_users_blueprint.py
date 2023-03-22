from application import application
from application.structure import structure
from domain.entities.auth import TokensPayload
from domain.utils import constants
from tests.factories.users import UserFactory


class TestUsersBlueprint():
    def setup_method(self):
        self.client = application.test_client()
        self.context = application.app_context()
        self.context.push()

        self.users_repository = structure.users_repository

    def teardown_method(self):
        self.users_repository.collection.delete_many({})
        self.context.pop()

    def test_create_user_invalid_principal(self):
        headers = {"Authorization": "test_access"}

        response = self.client.post(
            "/v1/users",
            headers=headers,
            json={},
            content_type="application/json"
        )

        assert response.status_code == 401
        assert response.json == {}

    def test_create_user_invalid(self):
        user = UserFactory.admin()
        user_id = self.users_repository.create(user)
        user.on_create(user_id)
        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
        user.on_login(tokens_pair)
        self.users_repository.update(user)

        body = {}
        headers = {
            "Authorization": f"{structure.principal_util.allowed_token_type} {tokens_pair.access}"
        }

        response = self.client.post(
            "/v1/users",
            json=body,
            headers=headers,
            content_type="application/json"
        )

        assert response.status_code == 400
        assert response.json == {
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

        body = {
            "role": constants.user_roles.community_social_worker,
            "email": f"test_{constants.user_roles.community_social_worker}@example.com",
            "password": "test_password",
            "first_name": "test_first_name",
            "last_name": "test_last_name"
        }
        headers = {
            "Authorization": f"{structure.principal_util.allowed_token_type} {tokens_pair.access}"
        }

        response = self.client.post(
            "/v1/users",
            json=body,
            headers=headers,
            content_type="application/json"
        )

        assert response.status_code == 200
        assert response.json["role"] == body["role"]
        assert response.json["email"] == body["email"]
        assert response.json["profile"]["first_name"] == body["first_name"]
        assert response.json["profile"]["last_name"] == body["last_name"]
