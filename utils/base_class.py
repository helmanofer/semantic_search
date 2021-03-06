from abc import ABC

from utils.conf_util import read_app_yaml


class BaseClass(ABC):
    def __init__(self, name) -> None:
        self.name: str = name

    @property
    def conf(self):
        super_conf = getattr(super, 'conf', None)
        if callable(super_conf):
            config = super_conf

        if hasattr(super, 'conf'):
            pass
        config = read_app_yaml()
        return
