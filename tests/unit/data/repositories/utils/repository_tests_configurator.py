from mock import Mock, MagicMock


class RepositoryTestsConfigurator():
    def configure_mocks(self, pymongo_mock):
        self.scheme = "test_scheme"
        self.username = "test_username"
        self.password = "test_password"
        self.host = "test_host"
        self.port = "test_port"
        self.db_name = "test_db_name"
        self.collection_name = "test_collection_name"
        self.translator_mock = Mock()

        self.collection_mock = Mock()
        self.client_mock = MagicMock()
        self.db_mock = MagicMock()
        self.db_mock.__getitem__.return_value = self.collection_mock
        self.client_mock.__getitem__.return_value = self.db_mock
        pymongo_mock.MongoClient.return_value = self.client_mock
