import os

db_name = '.ptt_statistics.db'

try:
    db_path = os.path.join(os.getenv('HOME'), db_name)
except TypeError:
    db_path = db_name
