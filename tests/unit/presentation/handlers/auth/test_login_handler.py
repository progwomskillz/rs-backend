from mock import Mock, patch

from presentation.handlers.auth import LoginHandler


class TestLoginHandler():
    def setup_method(self):
        self.use_case_mock = Mock()
        self.presenter_mock = Mock()

        self.handler = LoginHandler(self.use_case_mock, self.presenter_mock)

    @patch("presentation.handlers.auth.login_handler.LoginRequest")
    def test_execute(self, LoginRequest_mock):
        login_request_mock = Mock()
        LoginRequest_mock.return_value = login_request_mock

        json_mock = Mock()
        email = "test@example.com"
        password = "test_password"
        json_mock.get.side_effect = [email, password]
        request_mock = Mock()
        request_mock.json = json_mock

        expected_result_mock = Mock()
        self.use_case_mock.login.return_value = expected_result_mock

        result = self.handler.execute(request_mock)

        assert result == expected_result_mock
        assert json_mock.get.call_count == 2
        json_mock.get.assert_any_call("email")
        json_mock.get.assert_any_call("password")
        LoginRequest_mock.assert_called_once_with(email, password)
        self.use_case_mock.login.assert_called_once_with(login_request_mock)
