#!/usr/bin/env python

import os
os.system("sudo apt-get -y install python3-pexpect")
os.system("sudo apt-get -y install awscli")

p = os.popen("aws sns create-topic --name my-topic")
fid = p.read()
fid = fid[22:34]
os.system("aws sns subscribe --topic-arn arn:aws:sns:us-east-1:%s:my-topic --protocol email --notification-endpoint 1090265975@qq.com"%(fid))

