class ConfigHandler:
    """
    Read/write accessor to a configuration source
    """

    def create(self):
        """
        Creates a configuration source (creating file/database table/etc.)
        """
        raise NotImplementedError

    def load(self):
        """
        Loads configuration from the source
        :return nested list/dict
        """
        raise NotImplementedError

    def dump(self, cfg):
        """
        Serializes and store the configuration to the source
        """
        raise NotImplementedError

    def destroy(self):
        """
        Destroys configuration source (removing it from disk/database/etc.)
        """
        raise NotImplementedError
