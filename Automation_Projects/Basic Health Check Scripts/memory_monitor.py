#!/usr/bin/env python
import sys, smtplib, os
from datetime import datetime

import conf



current_free = lambda t: int(t[2][3])

table = sys.stdin.read()
lines = [[cell for cell in line.split(' ') if cell]
         for line in table.split("\n")]

free = current_free(lines)

#print lines, free

f = open(os.path.join(conf.LOG_DIR, 'memory.log'), 'a+')
f.write('%sM - %s\r\n' % (free, datetime.now().strftime('%Y-%m-%d %H:%M')))
f.close()

if free < getattr(conf, 'MINIMUM_FREE_MEM', 100):
        # ALARM! ALARM!
        msg = "Subject: LOW MEM on " + conf.SERVER_NAME + "\n"
	msg += "\n"
        msg += table

        # get process status
        f = os.popen('ps -eo pmem,pcpu,rss,vsize,args | sort -k 1 -r -n')
        msg += "\n\nProcesses:\n\n"
        msg += f.read()
        msg += "\n\n"

	s = smtplib.SMTP(conf.EMAIL_HOST)
	s.sendmail(conf.FROM_EMAIL,
                   conf.RECIPIENTS,
                   msg)
        sys.exit(1)

sys.exit(0)