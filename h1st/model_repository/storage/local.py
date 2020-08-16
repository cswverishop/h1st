import os
from typing import Any, NoReturn
import cloudpickle
from .base import Storage


class LocalStorage(Storage):
    """
    Provide data storage on top of local file system
    """
    def __init__(self, storage_path=None):
        self.storage_path = storage_path

    def get_obj(self, name: str) -> Any:
        """
        Retrieve object value

        :param name: object name
        """
        key = self._to_key(name)
        if not os.path.exists(key):
            raise KeyError(name)

        with open(key, "rb") as f:
            return cloudpickle.load(f)

    def get_bytes(self, name: str) -> bytes:
        """
        Retrieve object value in bytes

        :param name: object name
        """
        key = self._to_key(name)
        if not os.path.exists(key):
            raise KeyError(name)

        with open(key, "rb") as f:
            return f.read()

    def set_obj(self, name: str, value: Any) -> NoReturn:
        """
        Set key value to a python object

        :param name: object name
        :param value: value in python object
        """
        key = self._to_key(name)

        os.makedirs(os.path.dirname(key), mode=0o777, exist_ok=True)
        with open(key, "wb") as f:
            return cloudpickle.dump(value, f)

    def set_bytes(self, name, value):
        """
        Set a key value to a list of bytes

        :param name: object name
        :param value: value in bytes
        """
        key = self._to_key(name)

        os.makedirs(os.path.dirname(key), mode=0o777, exist_ok=True)
        with open(key, "wb") as f:
            return f.write(value)

    def exists(self, name: str) -> bool:
        """
        Return true if object exists in the storage
        """
        key = self._to_key(name)
        return os.path.exists(key)

    def delete(self, name: str) -> NoReturn:
        """
        Delete an object in storage
        """
        key = self._to_key(name)

        if os.path.exists(key):
            os.remove(key)

    def _to_key(self, key):
        # TODO: make sure it is a safe name
        key = key.replace("..", "__").replace("::", "/")
        return f"{self.storage_path}/{key}"
