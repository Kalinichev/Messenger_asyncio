from asyncio import Protocol, CancelledError
from hashlib import pbkdf2_hmac
from binascii import hexlify
from sys import stdout
from client.utils.mixins import ConvertMixin, DbInterfaceMixin
from client.utils.client_messages import JimClientMessage


class ClientAuth(ConvertMixin, DbInterfaceMixin):
    def __init__(self, db_path, username=None, password=None):
        super().__init__(db_path)
        self.username = username
        self.password = password

    def authenticate(self):
        if self.username and self.password:
            usr = self.get_client_by_username(self.username)
            dk = pbkdf2_hmac('sha256', self.password.encode('utf-8'), 'salt'.encode('utf-8'), 100_000)
            hashed_password = hexlify(dk)

            if usr:
                if hashed_password == usr.password:
                    self.add_client_history(self.username)
                    return True
                return False
            else:
                print('New user!')
                self.add_client(self.username, hashed_password)
                self.add_client_history(self.username)
                return True
        else:
            return False


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

    async def get_from_console(self):
        while not self.conn_is_open:
            pass
        self.output = self.output_to_console
        self.output('{2} connected to {0}:{1}\n'.format(*self.sockname, self.user))

        while True:
            content = await self.loop.run_in_executor(None, input)

    def output_to_console(self, data):
        _data = data
        stdout.write(_data)
