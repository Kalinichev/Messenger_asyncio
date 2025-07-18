from client.database.controller import ClientMessages
from client.database.models import CBase
from client.client_config import ENCODING
from json import dumps, loads


class DbInterfaceMixin:
    def __init__(self, db_path):
        self._cm = ClientMessages(db_path, CBase, echo=False)

    def add_client(self, username, info=None):
        return self._cm.add_client(username, info)

    def get_client_by_username(self, username):
        return self._cm.get_client_by_username(username)

    def add_client_history(self, client_username, ip_addr='8.8.8.8'):
        return self._cm.add_client_history(client_username, ip_addr)

    def set_user_online(self, client_username):
        return self._cm.set_user_online(client_username)


class ConvertMixin:
    def _dict_to_bytes(self, msg_dict: dict) -> bytes:
        if isinstance(msg_dict, dict):
            jmessage = dumps(msg_dict)
            bmessage = jmessage.encode(ENCODING)
            return bmessage
        raise TypeError

    def _bytes_to_dict(self, msg_bytes):
        if isinstance(msg_bytes, bytes):
            jmessage = msg_bytes.decode(ENCODING)
            message = loads(jmessage)
            if isinstance(message, dict):
                return message
            raise TypeError
        raise TypeError
