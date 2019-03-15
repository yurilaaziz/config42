import pytest

import config42


class BestFramework:
    pass


def test_not_implemented_extension():
    app = BestFramework()
    with pytest.raises(NotImplementedError):
        _ = config42.ConfigManager(app, path="files/flask-app.yml")
