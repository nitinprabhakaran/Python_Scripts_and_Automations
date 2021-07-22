#!/usr/bin/env python
import sys, smtplib, os
from datetime import datetime

import conf




table = sys.stdin.read()
lines = [[cell for cell in line.split(' ') if cell]
         for line in table.split("\n")]

# get percentage usage and gb free
if len(lines[1]) >= 3:
    usage = int(lines[1][4].replace('%', ''))
    free = lines[1][3]
else:
    usage = int(lines[2][3].replace('%', ''))
    free = lines[2][2]

f = open(os.path.join(conf.LOG_DIR, 'disk.log'), 'a+')
f.write('%s%% used %s free - %s\r\n' % (usage, free, datetime.now().strftime('%Y-%m-%d %H:%M')))
f.close()

if usage > getattr(conf, 'MAX_DISK_USAGE', 90):
        # ALARM! ALARM!
        msg = "Subject: LOW DISK SPACE on " + conf.SERVER_NAME + "\n"
	msg += "\n"
        msg += table

        # get process status
        for dir in getattr(conf, 'DISK_CHECK_DIRS', []):
            f = os.popen('du -s %s | sort -k 1 -r -n' % dir)
            msg += "\n\n%s usage:\n\n" % dir
            msg += f.read()
            msg += "\n\n"

	s = smtplib.SMTP(conf.EMAIL_HOST)
	s.sendmail(conf.FROM_EMAIL,
                   conf.RECIPIENTS,
                   msg)
        sys.exit(1)

sys.exit(0)