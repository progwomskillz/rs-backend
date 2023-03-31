import sys

from application.structure import structure
from domain.entities.users import (
    User,
    AdminProfile,
    CommunitySocialWorkerProfile,
    PublicOfficialProfile
)
from domain.utils import constants


role = ""
username = ""
password = ""
first_name = ""
last_name = ""

profiles_classes = {
    constants.user_roles.admin: {
        "class": AdminProfile,
        "args": [first_name, last_name]
    },
    constants.user_roles.community_social_worker: {
        "class": CommunitySocialWorkerProfile,
        "args": [first_name, last_name]
    },
    constants.user_roles.public_official: {
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
    username,
    structure.bcrypt_wrapper.hash(password),
    [],
    profile
)
structure.mongo_users_repository.create(user)
