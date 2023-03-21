import sys

from application.structure import structure
from domain.entities.users import (
    User,
    AdminProfile,
    CommunitySocialWorkerProfile,
    PublicOfficialProfile
)


role = ""
email = ""
password = ""
first_name = ""
last_name = ""

profiles_classes = {
    "admin": {
        "class": AdminProfile,
        "args": [first_name, last_name]
    },
    "community_social_worker": {
        "class": CommunitySocialWorkerProfile,
        "args": [first_name, last_name]
    },
    "public_official": {
        "class": PublicOfficialProfile,
        "args": [first_name, last_name]
    }
}

profile_constructor = profiles_classes.get(role)

if not profile_constructor:
    valid_roles = ", ".join(list(profiles_classes.keys()))
    print(f"Invalid role. Valid roles: {valid_roles}")
    sys.exit()

profile = profile_constructor["class"](*profile_constructor["args"])

user = User(
    None,
    role,
    email,
    structure.bcrypt_wrapper.hash(password),
    [],
    profile
)
structure.users_repository.create(user)
