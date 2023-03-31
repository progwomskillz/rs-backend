from data.translators.mongo.users import (
    MongoAdminProfileTranslator,
    MongoCommunitySocialWorkerProfileTranslator,
    MongoPublicOfficialProfileTranslator
)
from domain.entities.users import (
    AdminProfile,
    CommunitySocialWorkerProfile,
    PublicOfficialProfile
)
from tests.factories.users import ProfilesFactory


class TestMongoAdminProfileTranslator():
    def setup_method(self):
        self.translator = MongoAdminProfileTranslator()

    def test_from_document(self):
        document = {
            "first_name": "test_first_name",
            "last_name": "test_last_name"
        }

        result = self.translator.from_document(document)

        assert isinstance(result, AdminProfile) is True
        assert result.first_name == document["first_name"]
        assert result.last_name == document["last_name"]

    def test_to_document(self):
        profile = ProfilesFactory.admin()

        result = self.translator.to_document(profile)

        assert result == {
            "first_name": profile.first_name,
            "last_name": profile.last_name
        }


class TestMongoCommunitySocialWorkerProfileTranslator():
    def setup_method(self):
        self.translator = MongoCommunitySocialWorkerProfileTranslator()

    def test_from_document(self):
        document = {
            "first_name": "test_first_name",
            "last_name": "test_last_name"
        }

        result = self.translator.from_document(document)

        assert isinstance(result, CommunitySocialWorkerProfile) is True
        assert result.first_name == document["first_name"]
        assert result.last_name == document["last_name"]

    def test_to_document(self):
        profile = ProfilesFactory.community_social_worker()

        result = self.translator.to_document(profile)

        assert result == {
            "first_name": profile.first_name,
            "last_name": profile.last_name
        }


class TestMongoPublicOfficialProfileTranslator():
    def setup_method(self):
        self.translator = MongoPublicOfficialProfileTranslator()

    def test_from_document(self):
        document = {
            "first_name": "test_first_name",
            "last_name": "test_last_name"
        }

        result = self.translator.from_document(document)

        assert isinstance(result, PublicOfficialProfile) is True
        assert result.first_name == document["first_name"]
        assert result.last_name == document["last_name"]

    def test_to_document(self):
        profile = ProfilesFactory.public_official()

        result = self.translator.to_document(profile)

        assert result == {
            "first_name": profile.first_name,
            "last_name": profile.last_name
        }
