from argparse import ArgumentParser
from asyncio import get_event_loop

from server.server_config import DB_PATH, PORT
from server.utils.server_proto import ChatServerProtocol


class ConsoleServerApp:
    """Console server"""

    def __init__(self, pasrsed_args, db_path):
        self.args = pasrsed_args
        self.db_path = db_path
        self.ins = None

    def main(self):
        connections = dict()
        users = dict()
        loop = get_event_loop()

        # Each client will create a new protocol instance
        self.ins = ChatServerProtocol(self.db_path, connections, users)
        coro = loop.create_server(lambda: self.ins, self.args['addr'], self.args['port'])
        server = loop.run_until_complete(coro)

        # Serve requests until Ctrl+C
        print('Serving on {}:{}'.format(*server.sockets[0].getsockname()))
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass

        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()
