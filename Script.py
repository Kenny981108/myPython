#!/user/bin/env python

#setup the LAMP
import os
os.system("sudo apt-get update")
os.system("sudo bash myPython/mysql.sh")

os.system("sudo apt -y install apache2 php7.2 libapache2-mod-php")
os.system("sudo apt -y install graphviz aspell ghostscript clamav php7.2-pspell php7.2-bcmath php7.2-curl php7.2-gd php7.2-intl php7.2-mysql php7.2-xml php7.2-xmlrpc php7.2-ldap php7.2-zip php7.2-soap php7.2-mbstring")
os.system("sudo service apache2 restart")
os.system("sudo apt -y install git")
os.system("sudo apt -y install python3-mysqldb")
os.system("sudo apt-get -y install awscli")
os.chdir("/opt")
os.system("sudo git clone git://git.moodle.org/moodle.git")
os.chdir("moodle")
os.system("sudo git branch -a")
os.system("sudo git branch --track MOODLE_37_STABLE origin/MOODLE_37_STABLE")
os.system("sudo git checkout MOODLE_37_STABLE")
os.system("sudo cp -R /opt/moodle /var/www/html/")
os.system("sudo mkdir /var/moodledata")
os.system("sudo chown -R www-data /var/moodledata")
os.system("sudo chmod -R 777 /var/moodledata")

#modify the mysqld.conf file
fp = open('/etc/mysql/mysql.conf.d/mysqld.cnf','r')
lines = []
for line in fp:                  #内置的迭代器, 效率很高
    lines.append(line)
fp.close()

lines.insert(39, 'default_storage_engine = innodb\ninnodb_file_per_table = 1\ninnodb_file_format = Barracuda\n') #在第 LINE+1 行插入
s = ''.join(lines)
fp = open('/etc/mysql/mysql.conf.d/mysqld.cnf', 'w+')
fp.write(s)
fp.close()
del lines[:]
os.system("sudo service mysql restart")
#os.system("sudo python3 myPython/mysql.py")

#creat and setup mysql
import MySQLdb
db = MySQLdb.connect("localhost","root","1stgroup","mysql",charset = "utf8")
cursor = db.cursor()
cursor.execute("CREATE DATABASE moodle DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
cursor.execute("create user 'user1'@'localhost' IDENTIFIED BY '981204';")
cursor.execute("GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,CREATE TEMPORARY TABLES,DROP,INDEX,ALTER ON moodle.* TO user1@localhost IDENTIFIED BY '981204';")
db.close()

#create the config.php in moodle  
os.chdir("/var/www/html/moodle")
os.system("sudo touch config.php")
#setup the config.php
p = os.popen("curl ifconfig.me")
publicIP = p.read()
f = open('/var/www/html/moodle/config.php','w')
f.write("<?php  // Moodle configuration file \n"
         "\n"
        "unset($CFG);\n"
        "global $CFG;\n"
        "$CFG = new stdClass();\n"
        "\n"
        "$CFG->dbtype    = 'mysqli';\n"
        "$CFG->dblibrary = 'native';\n"
        "$CFG->dbhost    = 'localhost';\n"
        "$CFG->dbname    = 'mysql';\n"
        "$CFG->dbuser    = 'root';\n"
        "$CFG->dbpass    = '1stgroup';\n"
        "$CFG->prefix    = 'mdl_';\n"
        "$CFG->dboptions = array (\n"
         " 'dbpersist' => 0,\n"
          "  'dbport' => '',\n"
           "   'dbsocket' => ''\n,"
            "    'dbcollation' => 'utf8mb4_unicode_ci',\n"
             "   );\n"
              "   \n"
                "$CFG->wwwroot   = 'http://%s/moodle';\n"
                "$CFG->dataroot  = '/var/moodledata';\n"
                "$CFG->admin     = 'admin';\n"
                "\n"
                "$CFG->directorypermissions = 0777;\n"
                 "\n"
                "require_once(__DIR__ . '/lib/setup.php');\n"
                 "\n"
                "// There is no php closing tag in this file,\n"
                "// it is intentional because it prevents trailing whitespace problems!\n"%(publicIP))
f.close()
os.system("sudo php /var/www/html/moodle/install.php")
#setup phpmyadmin
os.system("sudo bash /home/ubuntu/myPython/phpmyadmin.sh")

#change IP
file = open('/lib/systemd/system/rc.local.service','r')
lines = []
for line in file:            
    lines.append(line)
file.close()
lines.insert(24, '[Install]\nWantedBy=multi-user.target\nAlias=rc-local.service')
s = ''.join(lines)
file = open('/lib/systemd/system/rc.local.service', 'w+')
file.write(s)
file.close()
del lines[:]
os.system("sudo ln -s /lib/systemd/system/rc.local.service /etc/systemd/system/rc.local.service")
os.system("sudo touch /etc/rc.local")
os.system("sudo chmod +x /etc/rc.local")
fa = open('/etc/rc.local','w')
fa.write("#!/bin/bash\npython3 /home/ubuntu/myPython/changeIP.py\npython3 /home/ubuntu/myPython/m.py")
fa.close()

#setup ftp
os.system("sudo apt-get install vsftpd")
os.system("sudo wget http://www.net2ftp.com/download/net2ftp_v1.3.zip")
os.system("sudo pwconv")
os.system("sudo useradd -m student")
os.system("sudo bash /home/ubuntu/myPython/pwd.sh")
f=open('/etc/vsftpd.conf','r+')
flist=f.readlines()
flist[30]="write_enable=YES\n"
flist[34]="local_umask=022\n"
flist[113]="chroot_local_user=YES\n"
f=open('/etc/vsftpd.conf','w+')
f.writelines(flist)
os.system("sudo service vsftpd start")

#setup net2ftp
os.system("sudo apt install unzip")
os.system("sudo unzip net2ftp_v1.3.zip -d /var/www/html")
os.system("aws configure")
os.system("aws sns create-topic --name my-topic")
p2 = os.popen("ec2metadata --instance-id")
ec2ID = p2.read().strip()
p1 = os.popen("aws sns create-topic --name alarm")
arn = p1.read().strip()
email = "1090265975@qq.com"
os.system("aws sns subscribe --topic-arn %s --protocol email --notification-endpoint %s"%(arn,email)) # subscribe
os.system("aws cloudwatch put-metric-alarm --alarm-name cpu-mon+%s --alarm-description 'Alarm when CPU exceeds 70 percent' --metric-name CPUUtilization --namespace AWS/EC2 --statistic Average --period 300 --threshold 70 --comparison-operator GreaterThanThreshold --dimensions  Name=InstanceId,Value=%s --evaluation-periods 2 --alarm-actions %s --unit Percent"%(ec2ID,ec2ID,arn))
os.system("aws cloudwatch put-metric-alarm --alarm-name cpu-CreditUsage+%s --alarm-description 'Alarm when CPU Credit Usage exceeds 70 percent' --metric-name CPUCreditUsage --namespace AWS/EC2 --statistic Average --period 300 --threshold 70 --comparison-operator GreaterThanThreshold --dimensions  Name=InstanceId,Value=%s --evaluation-periods 2 --alarm-actions %s --unit Percent"%(ec2ID,ec2ID,arn))
os.system("aws cloudwatch put-metric-alarm --alarm-name networkIn+%s --alarm-description 'Alarm when NetWorkIn exceeds 70 percent' --metric-name NetworkIn --namespace AWS/EC2 --statistic Average --period 300 --threshold 70 --comparison-operator GreaterThanThreshold --dimensions  Name=InstanceId,Value=%s --evaluation-periods 2 --alarm-actions %s --unit Percent"%(ec2ID,ec2ID,arn))
os.system("aws cloudwatch put-metric-alarm --alarm-name networkOut+%s --alarm-description 'Alarm when NetWorkOut exceeds 70 percent' --metric-name NetworkOut --namespace AWS/EC2 --statistic Average --period 300 --threshold 70 --comparison-operator GreaterThanThreshold --dimensions  Name=InstanceId,Value=%s --evaluation-periods 2 --alarm-actions %s --unit Percent"%(ec2ID,ec2ID,arn))
os.system("aws cloudwatch put-metric-alarm --alarm-name DiskReadBytes+%s --alarm-description 'Alarm when DiskReadBytes exceeds 100MB' --metric-name DiskReadBytes --namespace AWS/EC2 --statistic Average --period 300 --threshold 100000000 --comparison-operator GreaterThanThreshold --dimensions  Name=InstanceId,Value=%s --evaluation-periods 2 --alarm-actions %s --unit Percent"%(ec2ID,ec2ID,arn))
os.system("aws cloudwatch put-metric-alarm --alarm-name DiskWriteBytes+%s --alarm-description 'Alarm when DiskWriteBytes exceeds 100MB' --metric-name DiskWriteBytes --namespace AWS/EC2 --statistic Average --period 300 --threshold 100000000 --comparison-operator GreaterThanThreshold --dimensions  Name=InstanceId,Value=%s --evaluation-periods 2 --alarm-actions %s --unit Percent"%(ec2ID,ec2ID,arn))

