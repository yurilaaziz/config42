from pprint import pprint

from config42 import ConfigManager
from config42.handlers.argparse import ArgParse

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
        name="Action",
        key="action",
        choices=["create", "delete"],
        default="create"
    ), dict(
        name="logging level",
        key="logging.level",
        description="Logging verbosity level",
        choices=["critical", "error", "warning", "info", "debug"],
        type="string"

    )
]

try:
    config = ConfigManager(handler=ArgParse, schema=schema)
    pprint(config.as_dict())
except Exception as exc:
    pprint(exc)
