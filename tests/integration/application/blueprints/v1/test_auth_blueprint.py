from application import application
from application.structure import structure
from domain.entities.auth import TokensPayload
from tests.factories.users import UserFactory


class TestAuthBlueprint():
    def setup_method(self):
        self.client = application.test_client()
        self.context = application.app_context()
        self.context.push()

        self.users_repository = structure.mongo_users_repository

    def teardown_method(self):
        self.users_repository.collection.delete_many({})
        self.context.pop()

    def test_login_invalid_request(self):
        body = {}

        response = self.client.post(
            "/v1/auth/login",
            json=body,
            content_type="application/json"
        )

        assert response.status_code == 400
        assert response.json == {
            "username": [
                {
                    "message": "Has to be present",
                    "code": "presence"
                },
                {
                    "message": "Must be of type \"string\"",
                    "code": "type"
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
            ]
        }

    def test_login_user_not_found(self):
        body = {"username": "test_username", "password": "test_password"}

        response = self.client.post(
            "/v1/auth/login",
            json=body,
            content_type="application/json"
        )

        assert response.status_code == 401
        assert response.json == {}

    def test_login_wrong_password(self):
        user = UserFactory.admin()
        self.users_repository.create(user)
        body = {
            "username": user.username,
            "password": f"{UserFactory.get_password()}_wrong"
        }

        response = self.client.post(
            "/v1/auth/login",
            json=body,
            content_type="application/json"
        )

        assert response.status_code == 401
        assert response.json == {}

    def test_login(self):
        user = UserFactory.admin()
        self.users_repository.create(user)
        body = {
            "username": user.username,
            "password": UserFactory.get_password()
        }

        response = self.client.post(
            "/v1/auth/login",
            json=body,
            content_type="application/json"
        )

        assert response.status_code == 200
        assert list(response.json.keys()) == ["access", "refresh"]
        assert len(response.json["access"]) > 0
        assert len(response.json["refresh"]) > 0

    def test_refresh_invalid_refresh(self):
        body = {"refresh": "test_refresh"}

        response = self.client.post(
            "/v1/auth/refresh",
            json=body,
            content_type="application/json"
        )

        assert response.status_code == 401
        assert response.json == {}

    def test_refresh_user_not_found(self):
        tokens_payload = TokensPayload("test_user_id", "test_user_role")
        refresh = structure.jwt_wrapper.create_pair(tokens_payload).refresh
        body = {"refresh": refresh}

        response = self.client.post(
            "/v1/auth/refresh",
            json=body,
            content_type="application/json"
        )

        assert response.status_code == 401
        assert response.json == {}

    def test_refresh(self):
        user = UserFactory.admin()
        user_id = self.users_repository.create(user)
        user.on_create(user_id)
        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
        user.on_login(tokens_pair)
        self.users_repository.update(user)

        body = {"refresh": tokens_pair.refresh}

        response = self.client.post(
            "/v1/auth/refresh",
            json=body,
            content_type="application/json"
        )

        assert response.status_code == 200
        assert list(response.json.keys()) == ["access", "refresh"]
        assert len(response.json["access"]) > 0
        assert len(response.json["refresh"]) > 0

        user = self.users_repository.find_by_id(user.id)
        assert len(user.tokens_pairs) == 1
        new_tokens_pair = user.tokens_pairs[0]
        assert new_tokens_pair.access != tokens_pair.access
        assert new_tokens_pair.refresh == tokens_pair.refresh

    def test_logout_invalid(self):
        headers = {"Authorization": "test_refresh"}

        response = self.client.post(
            "/v1/auth/logout",
            headers=headers,
            content_type="application/json"
        )

        assert response.status_code == 401
        assert response.json == {}

    def test_logout(self):
        user = UserFactory.admin()
        user_id = self.users_repository.create(user)
        user.on_create(user_id)
        tokens_payload = TokensPayload(user.id, user.role)
        tokens_pair = structure.jwt_wrapper.create_pair(tokens_payload)
        user.on_login(tokens_pair)
        self.users_repository.update(user)

        headers = {
            "Authorization": f"{structure.principal_util.allowed_token_type} {tokens_pair.access}"
        }

        response = self.client.post(
            "/v1/auth/logout",
            headers=headers,
            content_type="application/json"
        )

        assert response.status_code == 200
        assert response.json == {}

        user = self.users_repository.find_by_id(user.id)
        assert len(user.tokens_pairs) == 0
