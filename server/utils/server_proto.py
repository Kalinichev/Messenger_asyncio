from asyncio import Protocol
from server.utils.mixins import ConvertMixin, DbInterfaceMixin
from server.utils.server_messages import JimServerMessage
from hashlib import pbkdf2_hmac
from binascii import hexlify


class ChatServerProtocol(Protocol, ConvertMixin, DbInterfaceMixin):
    """ A Server Protocol listening for subscriber messages """

    def __init__(self, db_path, connections, users):
        super().__init__(db_path)
        self.connections = connections
        self.users = users
        self.jim = JimServerMessage()
        self.user = None
        self.transport = None

    def connection_made(self, transport):
        """ Called when connection is initiated """
        self.connections[transport] = {
            'peername': transport.get_extra_info('peername'),
            'username': '',
            'transport': transport
        }
        self.transport = transport

    def authenticate(self, username, password):
        """Check user in DB"""
        if username and password:
            usr = self.get_client_by_username(username)
            dk = pbkdf2_hmac('sha256', password.encode('utf-8'), 'salt'.encode('utf-8'), 100_000)
            hashed_password = hexlify(dk)

            if usr:
                if hashed_password == usr.password:
                    self.add_client_history(username)
                    return True
                return False
            print('New user!')
            self.add_client(username, hashed_password)
            self.add_client_history(username)
            return True
        return False
