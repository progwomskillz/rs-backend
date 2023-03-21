import json
from abc import ABC, abstractmethod

from flask import Response

from domain.entities.exceptions import (
    InvalidRequest,
    UnauthenticatedException,
    UnauthorizedException,
    NotFoundException
)


class BaseHandler(ABC):
    def __init__(self, use_case, presenter):
        self.use_case = use_case
        self.presenter = presenter

    @abstractmethod
    def execute(self, request):
        pass

    def handle(self, request):
        if not hasattr(request, "principal"):
            request.principal = None
        try:
            result = self.execute(request)
            body = {}
            if self.presenter:
                body = self.presenter.present(result, request.principal)
            response = {"status": 200, "body": body}
        except InvalidRequest as e:
            response = {"status": 400, "body": e.errors}
        except UnauthenticatedException:
            response = {"status": 401, "body": {}}
        except UnauthorizedException:
            response = {"status": 403, "body": {}}
        except NotFoundException:
            response = {"status": 404, "body": {}}
        return Response(
            json.dumps(response["body"]),
            status=response["status"],
            mimetype="application/json"
        )
