import os

def play_mpg123(file_path):
    os.system("mpg123 {} > /dev/null 2>&1".format(file_path))
