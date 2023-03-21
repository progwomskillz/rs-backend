from mock import Mock, patch

from presentation.utils import PrincipalUtil


class TestPrincipalUtil():
    def setup_method(self):
        self.allowed_token_type = "Bearer"
        self.tokens_util_mock = Mock()
        self.users_repository_mock = Mock()

        self.util = PrincipalUtil(
            self.allowed_token_type,
            self.tokens_util_mock,
            self.users_repository_mock
        )

    def test_init(self):
        assert self.util.allowed_token_type == self.allowed_token_type.lower()
        assert self.util.tokens_util == self.tokens_util_mock
        assert self.util.users_repository == self.users_repository_mock

    def test_get_authorization_header_not_str(self):
        authorization_header = 123

        result = self.util.get(authorization_header)

        assert result is None
        self.tokens_util_mock.decode.assert_not_called()
        self.users_repository_mock.find_by_id.assert_not_called()

    def test_get_authorization_header_len_not_2(self):
        authorization_header = "token"

        result = self.util.get(authorization_header)

        assert result is None
        self.tokens_util_mock.decode.assert_not_called()
        self.users_repository_mock.find_by_id.assert_not_called()

    def test_get_invalid_token_type(self):
        authorization_header = "token test_token"

        result = self.util.get(authorization_header)

        assert result is None
        self.tokens_util_mock.decode.assert_not_called()
        self.users_repository_mock.find_by_id.assert_not_called()

    def test_get_invalid_token_payload(self):
        token = "test_token"
        authorization_header = f"{self.allowed_token_type} {token}"

        self.tokens_util_mock.decode.return_value = None

        result = self.util.get(authorization_header)

        assert result is None
        self.tokens_util_mock.decode.assert_called_once_with(token)
        self.users_repository_mock.find_by_id.assert_not_called()

    def test_get_user_not_found(self):
        token = "test_token"
        authorization_header = f"{self.allowed_token_type} {token}"

        user_id = "test_user_id"
        tokens_payload_mock = Mock()
        tokens_payload_mock.user_id = user_id
        self.tokens_util_mock.decode.return_value = tokens_payload_mock
        self.users_repository_mock.find_by_id.return_value = None

        result = self.util.get(authorization_header)

        assert result is None
        self.tokens_util_mock.decode.assert_called_once_with(token)
        self.users_repository_mock.find_by_id.assert_called_once_with(user_id)

    def test_get_tokens_pair_not_found(self):
        token = "test_token"
        authorization_header = f"{self.allowed_token_type} {token}"

        user_id = "test_user_id"
        tokens_payload_mock = Mock()
        tokens_payload_mock.user_id = user_id
        self.tokens_util_mock.decode.return_value = tokens_payload_mock
        user_mock = Mock()
        user_mock.tokens_pairs = []
        self.users_repository_mock.find_by_id.return_value = user_mock

        result = self.util.get(authorization_header)

        assert result is None
        self.tokens_util_mock.decode.assert_called_once_with(token)
        self.users_repository_mock.find_by_id.assert_called_once_with(user_id)

    @patch("presentation.utils.principal_util.Principal")
    def test_get(self, Principal_mock):
        token = "test_token"
        authorization_header = f"{self.allowed_token_type} {token}"

        user_id = "test_user_id"
        tokens_payload_mock = Mock()
        tokens_payload_mock.user_id = user_id
        self.tokens_util_mock.decode.return_value = tokens_payload_mock
        tokens_pair_mock_1 = Mock()
        tokens_pair_mock_1.access = f"{token}_1"
        tokens_pair_mock_1.refresh = "test_refresh_1"
        tokens_pair_mock_2 = Mock()
        tokens_pair_mock_2.access = token
        tokens_pair_mock_2.refresh = "test_refresh_2"
        tokens_pairs = [tokens_pair_mock_1, tokens_pair_mock_2]
        user_mock = Mock()
        user_mock.tokens_pairs = tokens_pairs
        self.users_repository_mock.find_by_id.return_value = user_mock
        principal_mock = Mock()
        Principal_mock.return_value = principal_mock

        result = self.util.get(authorization_header)

        assert result == principal_mock
        self.tokens_util_mock.decode.assert_called_once_with(token)
        self.users_repository_mock.find_by_id.assert_called_once_with(user_id)
        Principal_mock.assert_called_once_with(user_mock, tokens_pair_mock_2)
