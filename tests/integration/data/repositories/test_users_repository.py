from application.structure import structure
from domain.entities.users import User
from domain.entities.shared import Page
from tests.factories.users import UserFactory


class TestUsersRepository():
    def setup_method(self):
        self.repository = structure.users_repository

    def teardown_method(self):
        self.repository.collection.delete_many({})

    def test_find_by_email_not_found(self):
        email = "test@wxample.com"

        result = self.repository.find_by_email(email)

        assert result is None

    def test_find_by_email(self):
        user = UserFactory.admin()
        user_id = self.repository.create(user)
        user.on_create(user_id)

        result = self.repository.find_by_email(user.email)

        assert isinstance(result, User) is True
        assert result.email == user.email
        assert result.id == user.id

    def test_get_page_by_role_not_found(self):
        self.repository.create(UserFactory.admin())
        self.repository.create(UserFactory.admin())
        self.repository.create(UserFactory.admin())

        role = "test_role"
        page = 2
        page_size = 10

        result = self.repository.get_page_by_role(role, page, page_size)

        assert isinstance(result, Page) is True
        assert result.items == []
        assert result.page == page
        assert result.page_count == 1

    def test_get_page_by_role(self):
        users = [UserFactory.admin(), UserFactory.admin(), UserFactory.admin()]
        for user in users:
            user_id = self.repository.create(user)
            user.on_create(user_id)
        for _ in range(5):
            self.repository.collection.insert_one({"role": "test_role"})

        role = users[0].role
        page = 1
        page_size = 10

        result = self.repository.get_page_by_role(role, page, page_size)

        result = self.repository.get_page_by_role(role, page, page_size)

        assert isinstance(result, Page) is True
        assert len(result.items) == len(users)
        assert result.page == page
        assert result.page_count == 1
