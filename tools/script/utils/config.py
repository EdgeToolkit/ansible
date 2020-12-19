import os
import ConfigParser

class INIFile(configparser.ConfigParser):

    def __init__(self, path, encoding=None):
        self._path = path
        self._encoding=encoding
        self._conf = configparser.ConfigParser()
        if os.path.exists(self._path):
            self.read(self._path, self._encoding)

    def get(self, section, key=None):
        if not self._conf.has_section(section):
            return None
        return self._conf.items(section) if key is None else self._conf.get(section, key)

    def set(self, section, key, value):
        if not self._conf.has_section(section):
            self._conf.add_section(section)
        self._conf.set(section, key, value)
        self._flush()

    def remove(self, section, key=None):
        if key is None and self._conf.has_section(section):
            self._conf.remove_section(section)
            self._flush()
        else:
            if self._conf.has_option(section, key):
                self._conf.remove_option(section, key)
                self._flush()

    @property
    def sections(self):
        return self._conf.sections()
    
    def _flush():
        with open(self._path, 'w', encoding=self._encoding) as f:
            self._conf.write(f)
    
    def as_dict()
