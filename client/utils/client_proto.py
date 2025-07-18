from asyncio import Protocol, CancelledError
from hashlib import pbkdf2_hmac
from binascii import hexlify
from sys import stdout
from client.utils.mixins import ConvertMixin, DbInterfaceMixin
from client.utils.client_messages import JimClientMessage


class ChatClientProtocol(Protocol, ConvertMixin, DbInterfaceMixin):
    def __init__(self, db_path, loop, username=None, password=None, gui_instance=None, **kwargs):
        super().__init__(db_path)
        self.user = username
        self.password = password
        self.jim = JimClientMessage()
        self.conn_is_open = False
        self.loop = loop
        self.sockname = None
        self.transport = None
        self.output = None

    def connection_made(self, transport):
        self.sockname = transport.get_extra_info('sockname')
        self.transport = transport
        self.send_auth(self.user, self.password)
        self.conn_is_open = True

    def send_auth(self, user, password):
        if user and password:
            self.transport.write(self._dict_to_bytes(self.jim.auth(user, password)))

    def data_received(self, data):
        msg = self._bytes_to_dict(data)
        if msg:
            try:
                if msg['action'] == 'probe':
                    self.transport.write(self._dict_to_bytes(
                        self.jim.presence(self.user, status='connected from {0}, {1}'.format(*self.sockname))))
                elif msg['action'] == 'response':
                    if msg['code'] == 200:
                        pass
                    elif msg['code'] == 402:
                        self.connection_lost(CancelledError)
                    else:
                        self.output(msg)
            except Exception as e:
                print(e)
