from mock import Mock, patch

from presentation.handlers.auth_base_handler import AuthBaseHandler


class AuthBaseHandlerImp(AuthBaseHandler):
    def execute(self, request):
        return self.use_case.handle()


class TestAuthBaseHandler():
    def setup_method(self):
        self.use_case_mock = Mock()
        self.presenter_mock = Mock()
        self.principal_util_mock = Mock()

        self.handler = AuthBaseHandlerImp(
            self.use_case_mock,
            self.presenter_mock,
            self.principal_util_mock
        )

    def test_init(self):
        assert self.handler.principal_util == self.principal_util_mock

    @patch("presentation.handlers.base_handler.json")
    @patch("presentation.handlers.base_handler.Response")
    def test_handle_not_principal(self, Response_mock, json_mock):
        self.principal_util_mock.get.return_value = None

        request_mock = Mock()
        request_headers = {"Authorization": "token test_token"}
        request_mock.headers = request_headers

        use_case_result_mock = Mock()
        self.use_case_mock.handle.return_value = use_case_result_mock
        presented_result_mock = Mock()
        self.presenter_mock.present.return_value = presented_result_mock

        dumps_result_mock = Mock()
        json_mock.dumps.return_value = dumps_result_mock
        expected_result_mock = Mock()
        Response_mock.return_value = expected_result_mock

        result = self.handler.handle(request_mock)

        assert result == expected_result_mock
        self.principal_util_mock.get.assert_called_once_with(
            request_headers["Authorization"]
        )
        assert request_mock.principal is None
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
    def test_handle(self, Response_mock, json_mock):
        principal_mock = Mock()
        self.principal_util_mock.get.return_value = principal_mock

        request_mock = Mock()
        request_headers = {"Authorization": "token test_token"}
        request_mock.headers = request_headers

        use_case_result_mock = Mock()
        self.use_case_mock.handle.return_value = use_case_result_mock
        presented_result_mock = Mock()
        self.presenter_mock.present.return_value = presented_result_mock

        dumps_result_mock = Mock()
        json_mock.dumps.return_value = dumps_result_mock
        expected_result_mock = Mock()
        Response_mock.return_value = expected_result_mock

        result = self.handler.handle(request_mock)

        assert result == expected_result_mock
        self.principal_util_mock.get.assert_called_once_with(
            request_headers["Authorization"]
        )
        assert request_mock.principal == principal_mock
        self.use_case_mock.handle.assert_called_once()
        self.presenter_mock.present.assert_called_once_with(
            use_case_result_mock,
            principal_mock
        )
        json_mock.dumps.assert_called_once_with(presented_result_mock)
        Response_mock.assert_called_once_with(
            dumps_result_mock,
            status=200,
            mimetype="application/json"
        )
