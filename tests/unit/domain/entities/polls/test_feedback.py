from domain.entities.polls import Feedback


class TestFeedback():
    def setup_method(self):
        self.bothers = "test_bothers"
        self.age = 25

        self.entity = Feedback(self.bothers, self.age)

    def test_init(self):
        assert self.entity.bothers == self.bothers
        assert self.entity.age == self.age
