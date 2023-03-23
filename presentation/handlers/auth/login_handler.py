from ..base_handler import BaseHandler
from domain.entities.auth.requests import LoginRequest


class LoginHandler(BaseHandler):
    def execute(self, request):
        login_request = LoginRequest(
            request.json.get("username"),
            request.json.get("password")
        )
        return self.use_case.login(login_request)
