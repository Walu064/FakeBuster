import os


# Server
SERVER_HOST : str = '0.0.0.0'
SERVER_PORT : int = 7834

# Directories
cwd = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.dirname(os.path.dirname(cwd))

SCREENSHOTS_DIR : str = f'{root_dir}/data/screenshots'

if not os.path.exists(os.path.dirname(SCREENSHOTS_DIR)):
    os.mkdir(os.path.dirname(SCREENSHOTS_DIR))

if not os.path.exists(SCREENSHOTS_DIR):
    os.mkdir(SCREENSHOTS_DIR)