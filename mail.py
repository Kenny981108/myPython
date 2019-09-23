import smtplib
import sys
import email.mime.text

# my test mail
mail_username = 'xincancui9@gmail.com'
mail_password = 'cxc858019*'
from_addr = mail_username
to_addrs = ('1090265975@qq.com')

# HOST & PORT
HOST = 'smtp.gmail.com'
PORT = 25

# Create SMTP Object
smtp = smtplib.SMTP()
print 'connecting ...'

# show the debug log
smtp.set_debuglevel(1)

# connet
try:
    print smtp.connect(HOST, PORT)
except:
    print 'CONNECT ERROR ****'
# gmail uses ssl
smtp.starttls()
# login with username & password
try:
    print 'loginning ...'
    smtp.login(mail_username, mail_password)
except:
    print 'LOGIN ERROR ****'
# fill content with MIMEText's object
msg = email.mime.text.MIMEText('Hi ,I am leehark')
msg['From'] = from_addr
msg['To'] = ';'.join(to_addrs)
msg['Subject'] = 'hello , today is a special day'
print msg.as_string()
smtp.sendmail(from_addr, to_addrs, msg.as_string())
smtp.quit()
