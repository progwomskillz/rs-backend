class PollPresenter():
    def __init__(self, user_presenter, stats_presenter):
        self.user_presenter = user_presenter
        self.stats_presenter = stats_presenter

    def present(self, poll, principal):
        return {
            "id": poll.id,
            "user": self.user_presenter.present(poll.user, principal),
            "community_name": poll.community_name,
            "community_size": poll.community_size,
            "summary": [
                self.stats_presenter.present(stats, principal)
                for stats in poll.summary
            ]
        }
