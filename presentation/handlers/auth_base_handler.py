from .base_handler import BaseHandler


class AuthBaseHandler(BaseHandler):
    def __init__(self, use_case, presenter, principal_util):
        super().__init__(use_case, presenter)
        self.principal_util = principal_util

    def handle(self, request):
        request.principal = self.principal_util.get(
            request.headers.get("Authorization")
        )
        return super().handle(request)
