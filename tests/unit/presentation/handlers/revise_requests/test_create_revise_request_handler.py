from mock import Mock, patch

from presentation.handlers.revise_requests import CreateReviseRequestHandler


class TestCreateReviseRequestHandler():
    def setup_method(self):
        self.use_case_mock = Mock()
        self.presenter = None
        self.principal_util_mock = Mock()

        self.handler = CreateReviseRequestHandler(
            self.use_case_mock,
            self.presenter,
            self.principal_util_mock
        )

    @patch("presentation.handlers.revise_requests.create_revise_request_handler.CreateReviseRequestRequest")
    def test_execute(self, CreateReviseRequestRequest_mock):
        create_revise_request_request_mock = Mock()
        CreateReviseRequestRequest_mock.return_value =\
            create_revise_request_request_mock

        request_mock = Mock()
        principal_mock = Mock()
        request_mock.principal = principal_mock
        poll_id = "test_role"
        request_mock.json = {"poll_id": poll_id}

        expected_result_mock = Mock()
        self.use_case_mock.create_revise_request.return_value =\
            expected_result_mock

        result = self.handler.execute(request_mock)

        assert result == expected_result_mock
        CreateReviseRequestRequest_mock.assert_called_once_with(
            principal_mock,
            poll_id
        )
        self.use_case_mock.create_revise_request.assert_called_once_with(
            create_revise_request_request_mock
        )
