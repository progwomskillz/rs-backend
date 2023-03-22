from abc import ABC


class BaseProfilePresenter(ABC):
    def present(self, base_profile, principal):
        return {
            "first_name": base_profile.first_name,
            "last_name": base_profile.last_name
        }


class AdminProfilePresenter(BaseProfilePresenter):
    pass


class CommunitySocialWorkerProfilePresenter(BaseProfilePresenter):
    pass


class PublicOfficialProfilePresenter(BaseProfilePresenter):
    pass
