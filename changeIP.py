#!/usr/bin/python
import os
p = os.popen("curl ifconfig.me")
publicIP = p.read()
f=open('/var/www/html/moodle/config.php','r+')
flist=f.readlines()
flist[20]="$CFG->wwwroot   = 'http://%s/moodle';\n"%(publicIP)
f=open('/var/www/html/moodle/config.php','w+')
f.writelines(flist)

