import ntpath
import os

from .base import ConfigHandlerBase


class RawHandler(ConfigHandlerBase):
    def __init__(self, path):
        super().__init__()
        self.files = []
        self.path = path
        if os.path.isdir(self.path):
            self.root_directory = self.path
            for root, dirs, files in os.walk(self.path):
                for file in files:
                    self.files.append((file, os.path.join(root, file)))
        else:
            self.root_directory, file = ntpath.split(self.path)
            self.files.append((file, self.path))
        self.config = self.load()

    def load(self):
        result = {}
        for file, path in self.files:
            with open(path, "r", encoding="utf-8") as f:
                result.update({file: f.read()})
        return result

    def dump(self):
        for key, value in self.config.items():
            with open(os.path.join(self.root_directory, key), "w") as f:
                f.write(str(value))
        return True

    def destroy(self):
        if os.path.isdir(self.path):
            import shutil

            for root, dirs, files in os.walk(self.path):
                for dir in dirs:
                    shutil.rmtree(os.path.join(root, dir))
                for file in files:
                    os.remove(os.path.join(root, file))
        else:
            os.remove(self.path)
