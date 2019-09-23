#!/bin/bash

MAILLIST="xxxxx@xxx.cn"    #emailist

MEM_CORDON=100   #内存使用大于这个值报警
SWAP_CORDON=50  #交换区使用值大于这个报警  
CPU_CORDON=5    #cpu空闲小于这个值报警
DISK_CORDON=85  #磁盘占用大于这个值报警
HOSTNAME=`hostname`
DATA=`date`

send_warning()
{
    echo $MESSAGE | mutt -s "$TITLE" "$MAILLIST"
}

if [ $# -ne 0 ];then
    DISK_DIR=$1
else
    DISK_DIR="/dev/sdb1"
fi

#MEM|SWAP check
MEMSTATUS=`free | grep "Mem" | awk '{printf("%d", $3*100/$2)}'`
SWAPSTATUS=`free | grep "Swap" | awk '{printf("%d", $3*100/$2)}'`

if [ $MEMSTATUS -ge $MEM_CORDON ];then
    TITLE="[bad_news]:$HOSTNAME mem usage"
    MESSAGE="Time:${DATA},Mem_used:${MEMSTATUS}%,Swap_used:${SWAPSTATUS}%"
    send_warning
fi

if [ $SWAPSTATUS -ge $SWAP_CORDON ];then
    TITLE="[bad_news]:$HOSTNAME Swap usage"
    MESSAGE="Time:${DATA},Mem_used:${MEMSTATUS}%,Swap_used:${SWAPSTATUS}%"
    send_warning
fi   

#cpu

CPUSTATUS=`vmstat | awk '{print $15}' | tail -1`

if [ $CPUSTATUS -le $CPU_CORDON ];then
    TITLE="[bad_news]:$HOSTNAME cpu usage"
    MESSAGE="Time:${DATA},MCpu_free:${CPUSTATUS}%"
fi

#disk use n%

DISKSTATUS=`df -h $DISK_DIR | awk '{print $5}' | tail -1 | tr -d %`

if [ $DISKSTATUS -ge $DISK_CORDON ];then
    TITLE="[bad_news]:$HOSTNAME disk usage"
    MESSAGE="Time:${DATA},Disk_used:${DISKSTATUS}%"
    send_warning
fi

httpdnum=`ps aux | grep 'httpd' | wc -l`  
if [ $httpdnum -le 1 ]  
then  
    TITLE="[bad_news]:$HOSTNAME "
    MESSAGE="Time:${DATA},apache prograss is ended"
    send_warning
fi  

tomcatnum=`ps aux | grep 'tomcat' | wc -l`  
if [ $tomcatnum -le 1 ]  
then  
    TITLE="[bad_news]:$HOSTNAME "
    MESSAGE="Time:${DATA},tomcat prograss is ended"
    send_warning
fi   
