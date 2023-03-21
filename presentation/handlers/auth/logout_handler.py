from ..auth_base_handler import AuthBaseHandler
from domain.entities.auth.requests import LogoutRequest


class LogoutHandler(AuthBaseHandler):
    def execute(self, request):
        logout_request = LogoutRequest(request.principal)
        return self.use_case.logout(logout_request)
