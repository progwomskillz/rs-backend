from application import application


class TestGeneralBlueprint():
    def setup_method(self):
        self.client = application.test_client()
        self.context = application.app_context()
        self.context.push()

    def teardown_method(self):
        self.context.pop()

    def test_health_check(self):
        response = self.client.get("/health_check")

        assert response.status_code == 200
        assert response.json == {"message": "Healthy"}
