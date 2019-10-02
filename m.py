#!/usr/bin/env python
import os
#count=0
#if (count==0):
p2 = os.popen("ec2metadata --instance-id")
ec2ID = p2.read().strip()
p1 = os.popen("aws sns create-topic --name alarm")
arn = p1.read().strip()
#email = "1074623886@qq.com"
#os.system("aws sns subscribe --topic-arn %s --protocol email --notification-endpoint %s"%(arn,email)) # subscribe
os.system("aws cloudwatch put-metric-alarm --alarm-name cpu-mon+%s --alarm-description 'Alarm when CPU exceeds 70 percent' --metric-name CPUUtilization --namespace AWS/EC2 --statistic Average --period 300 --threshold 70 --comparison-operator GreaterThanThreshold --dimensions  Name=InstanceId,Value=%s --evaluation-periods 2 --alarm-actions %s --unit Percent"%(ec2ID,ec2ID,arn))
os.system("aws cloudwatch put-metric-alarm --alarm-name cpu-CreditUsage+%s --alarm-description 'Alarm when CPU Credit Usage exceeds 70 percent' --metric-name CPUCreditUsage --namespace AWS/EC2 --statistic Average --period 300 --threshold 70 --comparison-operator GreaterThanThreshold --dimensions  Name=InstanceId,Value=%s --evaluation-periods 2 --alarm-actions %s --unit Percent"%(ec2ID,ec2ID,arn))
os.system("aws cloudwatch put-metric-alarm --alarm-name cpu-mon+%s --alarm-description 'Alarm when CPU exceeds 70 percent' --metric-name CPUUtilization --namespace AWS/EC2 --statistic Average --period 300 --threshold 70 --comparison-operator GreaterThanThreshold --dimensions  Name=InstanceId,Value=%s --evaluation-periods 2 --alarm-actions %s --unit Percent"%(ec2ID,ec2ID,arn))
os.system("aws cloudwatch put-metric-alarm --alarm-name cpu-CreditUsage+%s --alarm-description 'Alarm when CPU Credit Usage exceeds 70 percent' --metric-name CPUCreditUsage --namespace AWS/EC2 --statistic Average --period 300 --threshold 70 --comparison-operator GreaterThanThreshold --dimensions  Name=InstanceId,Value=%s --evaluation-periods 2 --alarm-actions %s --unit Percent"%(ec2ID,ec2ID,arn))
os.system("aws cloudwatch put-metric-alarm --alarm-name networkIn+%s --alarm-description 'Alarm when NetWorkIn exceeds 70 percent' --metric-name NetworkIn --namespace AWS/EC2 --statistic Average --period 300 --threshold 70 --comparison-operator GreaterThanThreshold --dimensions  Name=InstanceId,Value=%s --evaluation-periods 2 --alarm-actions %s --unit Percent"%(ec2ID,ec2ID,arn))
os.system("aws cloudwatch put-metric-alarm --alarm-name networkOut+%s --alarm-description 'Alarm when NetWorkOut exceeds 70 percent' --metric-name NetworkOut --namespace AWS/EC2 --statistic Average --period 300 --threshold 70 --comparison-operator GreaterThanThreshold --dimensions  Name=InstanceId,Value=%s --evaluation-periods 2 --alarm-actions %s --unit Percent"%(ec2ID,ec2ID,arn))
os.system("aws cloudwatch put-metric-alarm --alarm-name DiskReadBytes+%s --alarm-description 'Alarm when DiskReadBytes exceeds 100MB' --metric-name DiskReadBytes --namespace AWS/EC2 --statistic Average --period 300 --threshold 100000000 --comparison-operator GreaterThanThreshold --dimensions  Name=InstanceId,Value=%s --evaluation-periods 2 --alarm-actions %s --unit Percent"%(ec2ID,ec2ID,arn))
os.system("aws cloudwatch put-metric-alarm --alarm-name DiskWriteBytes+%s --alarm-description 'Alarm when DiskWriteBytes exceeds 100MB' --metric-name DiskWriteBytes --namespace AWS/EC2 --statistic Average --period 300 --threshold 100000000 --comparison-operator GreaterThanThreshold --dimensions  Name=InstanceId,Value=%s --evaluation-periods 2 --alarm-actions %s --unit Percent"%(ec2ID,ec2ID,arn))
