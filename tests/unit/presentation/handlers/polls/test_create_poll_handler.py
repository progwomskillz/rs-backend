from mock import Mock, patch

from presentation.handlers.polls import CreatePollHandler


class TestCreatePollHandler():
    def setup_method(self):
        self.use_case_mock = Mock()
        self.presenter = None
        self.principal_util_mock = Mock()

        self.handler = CreatePollHandler(
            self.use_case_mock,
            self.presenter,
            self.principal_util_mock
        )

    @patch("presentation.handlers.polls.create_poll_handler.Feedback")
    @patch("presentation.handlers.polls.create_poll_handler.CreatePollRequest")
    def test_execute(self, CreatePollRequest_mock, Feedback_mock):
        create_poll_request_mock = Mock()
        CreatePollRequest_mock.return_value = create_poll_request_mock
        feedback_mock = Mock()
        Feedback_mock.return_value = feedback_mock

        request_mock = Mock()
        principal_mock = Mock()
        request_mock.principal = principal_mock
        community_name = "test_community_name"
        community_size = 25
        feedbacks = [{"bothers": "test_bothers", "age": 19}]
        request_mock.json = {
            "community_name": community_name,
            "community_size": community_size,
            "feedbacks": feedbacks
        }

        expected_result_mock = Mock()
        self.use_case_mock.create_poll.return_value = expected_result_mock

        result = self.handler.execute(request_mock)

        assert result == expected_result_mock
        CreatePollRequest_mock.assert_called_once_with(
            principal_mock,
            community_name,
            community_size,
            [feedback_mock]
        )
        Feedback_mock.assert_called_once_with(
            feedbacks[0]["bothers"],
            feedbacks[0]["age"]
        )
        self.use_case_mock.create_poll.assert_called_once_with(
            create_poll_request_mock
        )
