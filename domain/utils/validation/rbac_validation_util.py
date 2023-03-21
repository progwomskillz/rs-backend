from domain.entities.exceptions import UnauthorizedException


class RBACValidationUtil():
    def validate(self, user, roles):
        if user.role in roles:
            return
        raise UnauthorizedException()
