from mock import Mock, patch

from presentation.handlers.users import CreateUserHandler


class TestCreateUserHandler():
    def setup_method(self):
        self.use_case_mock = Mock()
        self.presenter = None
        self.principal_util_mock = Mock()

        self.handler = CreateUserHandler(
            self.use_case_mock,
            self.presenter,
            self.principal_util_mock
        )

    @patch("presentation.handlers.users.create_user_handler.CreateUserRequest")
    def test_execute(self, CreateUserRequest_mock):
        create_user_request_mock = Mock()
        CreateUserRequest_mock.return_value = create_user_request_mock

        request_mock = Mock()
        principal_mock = Mock()
        request_mock.principal = principal_mock
        role = "test_role"
        email = "test@example.com"
        password = "test_password"
        first_name = "test_first_name"
        last_name = "test_last_name"
        request_mock.json = {
            "role": role,
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name
        }

        expected_result_mock = Mock()
        self.use_case_mock.create_user.return_value = expected_result_mock

        result = self.handler.execute(request_mock)

        assert result == expected_result_mock
        CreateUserRequest_mock.assert_called_once_with(
            principal_mock,
            role,
            email,
            password,
            first_name,
            last_name
        )
        self.use_case_mock.create_user.assert_called_once_with(
            create_user_request_mock
        )
