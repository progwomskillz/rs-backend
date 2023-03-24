class PollPresenter():
    def __init__(self, stats_list_presenter):
        self.stats_list_presenter = stats_list_presenter

    def present(self, poll, principal):
        return {
            "id": poll.id,
            "community_name": poll.community_name,
            "community_size": poll.community_size,
            "summary": self.stats_list_presenter.present(
                poll.summary,
                principal
            )
        }
