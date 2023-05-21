# Config

## **Description:**

Directory contains required params to run server API.

## **Fields:**

1. Server:
    - *Host*: server API host IP address
    - *Port*: server API port

File: *`config.py`*

``` python
# Server
SERVER_HOST : str = '0.0.0.0'
SERVER_PORT : int = 7834
```

2. Directories:
    - *Screenshots*: directory for screenshots

File: *`config.py`*

``` python
import os

# Directories
cwd = os.path.dirname(os.path.realpath(__file__))
root_dir = os.path.dirname(os.path.dirname(cwd))

# Screenshots directory
SCREENSHOTS_DIR : str = f'{root_dir}/data/screenshots'

# Make directories if not exists
#   - /fakebuster/data
if not os.path.exists(os.path.dirname(SCREENSHOTS_DIR)):
    os.mkdir(os.path.dirname(SCREENSHOTS_DIR))

#   - /fakebuster/data/screenshots
if not os.path.exists(SCREENSHOTS_DIR):
    os.mkdir(SCREENSHOTS_DIR)
```
