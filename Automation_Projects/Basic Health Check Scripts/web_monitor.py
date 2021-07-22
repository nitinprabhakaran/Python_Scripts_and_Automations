#!/usr/bin/env python
from datetime import datetime
import httplib
import smtplib
import socket
import os
import time

import conf

WEB_TIMEOUT = getattr(conf, 'WEB_TIMEOUT', 10)
MAX_ATTEMPTS = 2

socket.setdefaulttimeout(WEB_TIMEOUT)

def get_status_code(host, path="/", attempts=0):
    """ This function retreives the status code of a website by requesting
        HEAD data from the host. This means that it only requests the headers.
        If the host cannot be reached or something else goes wrong, it returns
        None instead.
    """
    try:
        conn = httplib.HTTPConnection(host)
        conn.request("HEAD", path)
        status = conn.getresponse().status
        conn.close()
        if status == 405:
            conn = httplib.HTTPConnection(host)
            conn.request("GET", path)
            status = conn.getresponse().status
            conn.close()
    except socket.timeout, e:
        attempts += 1
        if attempts < MAX_ATTEMPTS:
            # pause then try again
            time.sleep(WEB_TIMEOUT)
            return get_status_code(host, path, attempts)
        else:
            return '%s (%s attempts)' % (e, attempts)
    except (StandardError, socket.gaierror, socket.error), e:
        return e
    else:
        return status

f = open(os.path.join(conf.LOG_DIR, 'web.log'), 'a+')
dead = []
for u in conf.URLS:
    domain = u.split('/')[0]
    path = '/' + '/'.join(u.split('/')[1:])
    status = get_status_code(domain, path)
    if status not in (200, '[Errno -3] Temporary failure in name resolution', '[Errno -2] Name or service not known'):
         dead.append((u, status)) 

    f.write('%s %s Status:%s\r\n' % (datetime.now().strftime('%Y-%m-%d %H:%M'), u, status))

f.close()

socket.setdefaulttimeout(30)

if len(dead):
    # ALARM! ALARM!
    msg = "Subject: WEB SERVER DOWN - %s\n" % ', '.join([d[0] for d in dead])
    msg += "\n"
    for d in dead:
        msg += "%s Status: %s\n" % d

    s = smtplib.SMTP(conf.EMAIL_HOST)
    s.sendmail(conf.FROM_EMAIL,conf.RECIPIENTS,msg)