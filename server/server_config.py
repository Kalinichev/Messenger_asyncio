from pathlib import Path

home = str(Path.home())

ENCODING = 'utf-8'
PORT = 14908

DB_PROTOCOL = 'sqlite:///'
DB_NAME = '/client_contacts.db'
DB_PATH = DB_PROTOCOL + home + DB_NAME
