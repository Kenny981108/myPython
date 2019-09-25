#!/usr/bin/env python

import os
os.system("sudo apt-get -y install python3-pexpect")
os.system("sudo apt-get -y install awscli")

import pexpect

process = pexpect.spawn("aws configure")
process.expect("AWS Access Key ID [None]:")
process.expect("AWS Secret Access Key [None]:")
process.expect("Default region name [None]:")
process.sendline("us-east-1")
process.expect("Default output format [None]:")
process.sendline("text")


p = os.popen("aws sns create-topic --name my-topic")
fid = p.read()
fid = fid[22:34]
os.system("aws sns subscribe --topic-arn arn:aws:sns:us-east-1:%s:my-topic --protocol email --notification-endpoint 1090265975@qq.com"%(fid))

