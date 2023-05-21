# Server
SERVER_HOST : str = '0.0.0.0'
SERVER_PORT : int = 7834


import os

# Directories
cwd = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.dirname(os.path.dirname(cwd))

SCREENSHOTS_DIR : str = f'{root_dir}\\data\\screenshots'

# Make directories if not exists
#   - /fakebuster/data
if not os.path.exists(os.path.dirname(SCREENSHOTS_DIR)):
    os.mkdir(os.path.dirname(SCREENSHOTS_DIR))

#   - /fakebuster/data/screenshots
if not os.path.exists(SCREENSHOTS_DIR):
    os.mkdir(SCREENSHOTS_DIR)