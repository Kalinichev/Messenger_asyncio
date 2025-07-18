from datetime import datetime as dt


class JimClientMessage:
    def auth(self, username, password):
        data = {
            'action': 'authenticate',
            'time': dt.now().timestamp(),
            'user': {
                'account_name': username,
                'password': password
            }
        }
        return data

    def presence(self, sender, status='Yep, I am here!'):
        data = {
            'action': 'presence',
            'time': dt.now().timestamp(),
            'type': 'status',
            'user': {
                'account_name': sender,
                'status': status
            }
        }
        return data
