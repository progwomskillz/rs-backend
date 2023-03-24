class ReviseRequestPresenter():
    def __init__(self, poll_presenter):
        self.poll_presenter = poll_presenter

    def present(self, revise_request, principal):
        return {
            "id": revise_request.id,
            "poll": self.poll_presenter.present(revise_request.poll, principal)
        }
