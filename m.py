#!/usr/bin/env python

import os
os.system("aws sns create-topic --name my-topic")
p = os.popen("aws sns create-topic --name my-topic")
fid = p.read()
fid = fid[22:34]
ec2 = os.popen("ec2metadata --instance-id")
ec2id = ec2.read()
ec2id = ec2id.strip('\n')
fa = os.popen('test -f /home/ubuntu/myPython/%s.txt && echo "exist" || echo "Not exist"'%(ec2id))
fa = fa.read()
fa = fa.strip()
if fa =="exist":
    print("well done")
elif fa == "Not exist":
    os.system("aws sns subscribe --topic-arn arn:aws:sns:us-east-1:%s:my-topic --protocol email --notification-endpoint 1090265975@qq.com"%(fid))
    os.system("aws cloudwatch put-metric-alarm --alarm-name cpu-mon --alarm-description 'Alarm when CPU exceeds 70%s' --metric-name CPUUtilization --namespace AWS/EC2 --statistic Average --period 300 --threshold 70 --comparison-operator GreaterThanThreshold --dimensions  Name=InstanceId,Value=%s --evaluation-periods 2 --alarm-actions arn:aws:sns:us-east-1:%s:my-topic  --unit Percent"%("%",ec2id,fid))
    os.system("aws cloudwatch put-metric-alarm --alarm-name ebs-mon --alarm-description 'Alarm when EBS volume exceeds 100MB throughput' --metric-name VolumeReadBytes --namespace AWS/EBS --statistic Average --period 300 --threshold 100000000 --comparison-operator GreaterThanThreshold --dimensions Name=VolumeId,Value=%s --evaluation-periods 3 --alarm-actions arn:aws:sns:us-east-1:%s:my-topic "%(ec2id,fid))
    os.system("sudo touch /home/ubuntu/myPython/%s.txt"%(ec2id))  
