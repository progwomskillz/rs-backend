class Constants():
    @property
    def user_roles(self):
        return UserRoles()


class UserRoles():
    @property
    def admin(self):
        return "admin"

    @property
    def community_social_worker(self):
        return "community_social_worker"

    @property
    def public_official(self):
        return "public_official"


constants = Constants()
