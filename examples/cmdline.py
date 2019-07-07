from config42 import ConfigManager
from config42.handlers.argparse import Argparse

schema = [
    dict(
        name="first name",
        key="user.firstname"
    ), dict(
        name="last name",
        key="user.lastname"
    ), dict(
        name="email",
        source=dict(argv=["-e", "--email"]),
        key="user.email",
        description="A valid email address"
    ), dict(
        key="action",
        choices=["create", "delete"],
    )
]

config = ConfigManager(handler=Argparse, schema=schema)

print(config.as_dict())
