from config42.handlers import ConfigHandler


class Defaults(ConfigHandler):
    """
    Memory based handler, used to store default configurations
    """

    def __init__(self, cfg=None):
        """
        :param cfg: nested dict/list
        """
        super().__init__()
        self.cfg = cfg

    def create(self):
        if self.cfg is None:
            self.cfg = {}

    def load(self):
        return self.cfg

    def dump(self, cfg):
        self.cfg = cfg

    def destroy(self):
        self.cfg = None
