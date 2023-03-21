from mock import Mock, patch

from presentation.handlers.base_handler import BaseHandler
from domain.entities.exceptions import (
    InvalidRequest,
    UnauthenticatedException,
    UnauthorizedException
)


class BaseHandlerImp(BaseHandler):
    def execute(self, request):
        return self.use_case.handle()


class TestBaseHandler():
    def setup_method(self):
        self.use_case_mock = Mock()
        self.presenter_mock = Mock()

        self.handler = BaseHandlerImp(self.use_case_mock, self.presenter_mock)

    def test_init(self):
        assert self.handler.use_case == self.use_case_mock
        assert self.handler.presenter == self.presenter_mock

    @patch("presentation.handlers.base_handler.json")
    @patch("presentation.handlers.base_handler.Response")
    def test_handle(self, Response_mock, json_mock):
        use_case_result_mock = Mock()
        self.use_case_mock.handle.return_value = use_case_result_mock
        presented_result_mock = Mock()
        self.presenter_mock.present.return_value = presented_result_mock

        dumps_result_mock = Mock()
        json_mock.dumps.return_value = dumps_result_mock
        expected_result_mock = Mock()
        Response_mock.return_value = expected_result_mock

        request_mock = Mock()
        del request_mock.principal

        result = self.handler.handle(request_mock)

        assert result == expected_result_mock
        self.use_case_mock.handle.assert_called_once()
        self.presenter_mock.present.assert_called_once_with(
            use_case_result_mock,
            None
        )
        json_mock.dumps.assert_called_once_with(presented_result_mock)
        Response_mock.assert_called_once_with(
            dumps_result_mock,
            status=200,
            mimetype="application/json"
        )

    @patch("presentation.handlers.base_handler.json")
    @patch("presentation.handlers.base_handler.Response")
    def test_handle_invalid_request(self, Response_mock, json_mock):
        errors = {"email": ["type"]}
        self.use_case_mock.handle.side_effect = [InvalidRequest(errors)]

        dumps_result_mock = Mock()
        json_mock.dumps.return_value = dumps_result_mock
        expected_result_mock = Mock()
        Response_mock.return_value = expected_result_mock

        request_mock = Mock()

        result = self.handler.handle(request_mock)

        assert result == expected_result_mock
        self.use_case_mock.handle.assert_called_once()
        self.presenter_mock.present.assert_not_called()
        json_mock.dumps.assert_called_once_with(errors)
        Response_mock.assert_called_once_with(
            dumps_result_mock,
            status=400,
            mimetype="application/json"
        )

    @patch("presentation.handlers.base_handler.json")
    @patch("presentation.handlers.base_handler.Response")
    def test_handle_unauthenticated_exception(self, Response_mock, json_mock):
        self.use_case_mock.handle.side_effect = [UnauthenticatedException()]

        dumps_result_mock = Mock()
        json_mock.dumps.return_value = dumps_result_mock
        expected_result_mock = Mock()
        Response_mock.return_value = expected_result_mock

        request_mock = Mock()

        result = self.handler.handle(request_mock)

        assert result == expected_result_mock
        self.use_case_mock.handle.assert_called_once()
        self.presenter_mock.present.assert_not_called()
        json_mock.dumps.assert_called_once_with({})
        Response_mock.assert_called_once_with(
            dumps_result_mock,
            status=401,
            mimetype="application/json"
        )

    @patch("presentation.handlers.base_handler.json")
    @patch("presentation.handlers.base_handler.Response")
    def test_handle_unauthorized_exception(self, Response_mock, json_mock):
        self.use_case_mock.handle.side_effect = [UnauthorizedException()]

        dumps_result_mock = Mock()
        json_mock.dumps.return_value = dumps_result_mock
        expected_result_mock = Mock()
        Response_mock.return_value = expected_result_mock

        request_mock = Mock()

        result = self.handler.handle(request_mock)

        assert result == expected_result_mock
        self.use_case_mock.handle.assert_called_once()
        self.presenter_mock.present.assert_not_called()
        json_mock.dumps.assert_called_once_with({})
        Response_mock.assert_called_once_with(
            dumps_result_mock,
            status=403,
            mimetype="application/json"
        )
