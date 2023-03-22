from ..auth_base_handler import AuthBaseHandler
from domain.entities.users.requests import CreateUserRequest


class CreateUserHandler(AuthBaseHandler):
    def execute(self, request):
        create_user_request = CreateUserRequest(
            request.principal,
            request.json.get("role"),
            request.json.get("email"),
            request.json.get("password"),
            request.json.get("first_name"),
            request.json.get("last_name")
        )
        return self.use_case.create_user(create_user_request)
