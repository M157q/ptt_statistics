import os


dir_name = 'ptt_statistics'
home_path = os.getenv('HOME')

if home_path:
    dir_path = os.path.join(home_path, '.'+dir_name)
else:
    dir_path = dir_name


db_name = 'ptt_statistics.db'
db_path = os.path.join(dir_path, db_name)

error_log_path = os.path.join(dir_path, 'error.log')
