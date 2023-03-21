from domain.entities.users import (
    AdminProfile,
    CommunitySocialWorkerProfile,
    PublicOfficialProfile
)


class AdminProfileTranslator():
    def from_document(self, document):
        return AdminProfile(
            document.get("first_name"),
            document.get("last_name"),
        )

    def to_document(self, admin_profile):
        return {
            "first_name": admin_profile.first_name,
            "last_name": admin_profile.last_name
        }


class CommunitySocialWorkerProfileTranslator():
    def from_document(self, document):
        return CommunitySocialWorkerProfile(
            document.get("first_name"),
            document.get("last_name"),
        )

    def to_document(self, admin_profile):
        return {
            "first_name": admin_profile.first_name,
            "last_name": admin_profile.last_name
        }


class PublicOfficialProfileTranslator():
    def from_document(self, document):
        return PublicOfficialProfile(
            document.get("first_name"),
            document.get("last_name"),
        )

    def to_document(self, admin_profile):
        return {
            "first_name": admin_profile.first_name,
            "last_name": admin_profile.last_name
        }
