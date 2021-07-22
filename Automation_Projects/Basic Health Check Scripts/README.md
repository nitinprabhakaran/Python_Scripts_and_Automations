# Settings

Create a conf.py containing these:

    SERVER_NAME = 'My Server'
    EMAIL_HOST = 'localhost'
    FROM_EMAIL = 'root@myserver.com'
    RECIPIENTS = ['me@example.com']
    LOG_DIR = '~/log'
    URLS = ('mydomain.com', 'myotherdomain.com/testurl')

Optional settings:

    WEB_TIMEOUT (default is 10)

# Usage

Add these to your crontab:


    *          *  *   *   *     free -m | /path/to/memory_monitor.py
    45         *  *   *   *     df -h | /path/to/disk_monitor.py
    15,35,55   *  *   *   *     /path/to/web_monitor.py