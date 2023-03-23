from domain.entities.polls import Feedback


class FeedbackFactory():
    @staticmethod
    def generic():
        return Feedback("family health", 24)

    @staticmethod
    def generate(bothers, age):
        return Feedback(bothers, age)
