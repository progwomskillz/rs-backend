class UserPresenter():
    def __init__(self, profile_presenters):
        self.profile_presenters = profile_presenters

    def present(self, user, principal):
        profile_presenter = self.profile_presenters[user.role]
        return {
            "id": user.id,
            "role": user.role,
            "username": user.username,
            "profile": profile_presenter.present(user.profile, principal)
        }
