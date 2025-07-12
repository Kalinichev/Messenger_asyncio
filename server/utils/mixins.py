from server.database.controller import ClientMessages
from server.database.models import CBase


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
