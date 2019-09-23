#!/usr/bin/env python

import os, time

import smtplib

from email.mime.text import MIMEText

#设置服务器所需信息
#163邮箱服务器地址
def send_mail(content):
    mail_host = 'smtp.163.com'  
    #163用户名
    mail_user = 'monitor383@163.com'  
    #密码(部分邮箱为授权码) 
    mail_pass = 'it123456'   
    #邮件发送方邮箱地址
    sender = 'monitor383@163.com'  
    #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = ['1090265975@qq.com']  

    #设置email信息
    #邮件内容设置
    message = MIMEText(content,'plain','utf-8')
    #邮件主题       
    message['Subject'] = 'Virtual Machine Alarm!' 
    #发送方信息
    message['From'] = sender 
    #接受方信息     
    message['To'] = receivers[0]  

    #登录并发送邮件
    try:
        smtpObj = smtplib.SMTP() 
        #连接到服务器
        smtpObj.connect(mail_host,25)
        #登录到服务器
        smtpObj.login(mail_user,mail_pass) 
        #发送
        smtpObj.sendmail(
            sender,receivers,message.as_string()) 
        #退出
        smtpObj.quit() 
        print('success')
    except smtplib.SMTPException as e:
        print('error',e) #打印错误
last_worktime=0
last_idletime=0

def get_cpu():
        global last_worktime, last_idletime
        f=open("/proc/stat","r")
        line=""
        while not "cpu " in line: line=f.readline()
        f.close()
        spl=line.split(" ")
        worktime=int(spl[2])+int(spl[3])+int(spl[4])
        idletime=int(spl[5])
        dworktime=(worktime-last_worktime)
        didletime=(idletime-last_idletime)
        rate=float(dworktime)/(didletime+dworktime)
        last_worktime=worktime
        last_idletime=idletime
        if(last_worktime==0): return 0
        return rate

def get_mem_usage_percent():
    try:
        f = open('/proc/meminfo', 'r')
        for line in f:
            if line.startswith('MemTotal:'):
                mem_total = int(line.split()[1])
            elif line.startswith('MemFree:'):
                mem_free = int(line.split()[1])
            elif line.startswith('Buffers:'):
                mem_buffer = int(line.split()[1])
            elif line.startswith('Cached:'):
                mem_cache = int(line.split()[1])
            elif line.startswith('SwapTotal:'):
                vmem_total = int(line.split()[1])
            elif line.startswith('SwapFree:'):
                vmem_free = int(line.split()[1])
            else:
                continue
        f.close()
    except:
        return None
    physical_percent = usage_percent(mem_total - (mem_free + mem_buffer + mem_cache), mem_total)
    virtual_percent = 0
    if vmem_total > 0:
        virtual_percent = usage_percent((vmem_total - vmem_free), vmem_total)
    return physical_percent, virtual_percent

def usage_percent(use, total):
    try:
        ret = (float(use) / total) * 100
    except ZeroDivisionError:
        raise Exception("ERROR - zero division error")
    return ret

statvfs = os.statvfs('/')

total_disk_space = statvfs.f_frsize * statvfs.f_blocks
free_disk_space = statvfs.f_frsize * statvfs.f_bfree
disk_usage = (total_disk_space - free_disk_space) * 100.0 / total_disk_space
disk_usage = int(disk_usage)
disk_tip = "硬盘空间使用率（最大100%）："+str(disk_usage)+"%"
print(disk_tip)

mem_usage = get_mem_usage_percent()
mem_usage = int(mem_usage[0])
mem_tip = "物理内存使用率（最大100%）："+str(mem_usage)+"%"
print(mem_tip)

cpu_usage = int(get_cpu()*100)
cpu_tip = "CPU使用率（最大100%）："+str(cpu_usage)+"%"
print(cpu_tip)

load_average = os.getloadavg()
load_tip = "系统负载（三个数值中有一个超过3就是高）："+str(load_average)
print(load_tip)


if disk_usage >= 0 and mem_usage >= 0 and cpu_usage >= 0:
    send_mail('This virtual machine has an alarm about disk usage, please check it soon. The disk uasge is %s' 
              '\nThis virtual machine has an alarm about CPU usage, please check it soon. The CPU uasge is %s' 
              '\nThis virtual machine has an alarm about Mem usage, please check it soon. The Mem uasge is %s',%(disk_tip,cpu_tip,mem_tip))
elif disk_usage < 0 and mem_usage < 0 and cpu_usage >= 0:
    send_mail('This virtual machine has an alarm about CPU usage, please check it soon. The CPU uasge is %s', %(cpu_tip))
elif disk_usage < 0 and mem_usage >= 0 and cpu_usage < 0:
    send_mail('This virtual machine has an alarm about Mem usage, please check it soon. The Mem uasge is %s', %(mem_tip))
elif disk_usage >= 0 and mem_usage < 0 and cpu_usage < 0:
    send_mail('This virtual machine has an alarm about disk usage, please check it soon. The disk uasge is %s', %(disk_tip))
elif disk_usage >= 0 and mem_usage < 0 and cpu_usage >= 0:
    send_mail('This virtual machine has an alarm about disk usage, please check it soon. The disk uasge is %s'
              '\nThis virtual machine has an alarm about CPU usage, please check it soon. The CPU uasge is %s', %(disk_tip,cpu_tip))
elif disk_usage >= 0 and mem_usage >= 0 and cpu_usage < 0:
    send_mail('This virtual machine has an alarm about disk usage, please check it soon. The disk uasge is %s'
             '\nThis virtual machine has an alarm about Mem usage, please check it soon. The Mem uasge is %s', %(disk_tip,mem_tip))
elif disk_usage < 0 and mem_usage >= 0 and cpu_usage >= 0:
    send_mail('\nThis virtual machine has an alarm about CPU usage, please check it soon. The CPU uasge is %s'
             '\nThis virtual machine has an alarm about Mem usage, please check it soon. The Mem uasge is %s', %(cpu_tip,mem_tip))

for i in range(3):
    if load_usage[i] >= 0:
        send_mail('This virtual machine has an alarm about load average, please check it soon. The load average is %s', %(load_tip))
        break
    

