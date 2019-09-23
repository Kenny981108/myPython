#!/usr/bin/env python

# your Gmail account  
import smtplib 
  
# creates SMTP session 
s = smtplib.SMTP('smtp.gmail.com', 587) 
  
# start TLS for security 
s.starttls() 
  
# Authentication 
s.login("xincancui9@gmail.com", "cxc858019*") 
  
# message to be sent 
message = "Message_you_need_to_send"
  
# sending the mail 
s.sendmail("xincancui9@gmai.com", "1090265975@qq.com", message) 
  
# terminating the session 
s.quit() 
