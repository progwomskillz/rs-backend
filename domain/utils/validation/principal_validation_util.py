from domain.entities.exceptions import UnauthenticatedException


class PrincipalValidationUtil():
    def validate(self, principal):
        if principal:
            return
        raise UnauthenticatedException()
