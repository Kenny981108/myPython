#!/usr/bin/env python

import os
os.system("sudo apt-get -y install python3-pexpect")
os.system("sudo apt-get -y install awscli")

import pexpect

process = pexpect.spawn("aws configure")
process.expect("AWS Access Key ID [None]:")
process.sendline("AKIAIP3LGYHOIKPQ55YQ")
process.expect("AWS Secret Access Key [None]:")
process.sendline("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")
process.expect("Default region name [None]:")
process.sendline("us-east-1")
process.expect("Default output format [None]:")
process.sendline("text")

returns = pexpect.run("aws sns create-topic --name my-topic")
fid = renturns[22:34]
os.system("aws sns subscribe --topic-arn arn:aws:sns:us-east-1:111122223333:my-topic --protocol email --notification-endpoint 1090265975@qq.com")
