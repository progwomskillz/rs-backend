from domain.entities.polls import Feedback


class FeedbackTranslator():
    def from_document(self, document):
        return Feedback(
            document.get("bothers"),
            document.get("age")
        )

    def to_document(self, feedback):
        return {
            "bothers": feedback.bothers,
            "age": feedback.age
        }
