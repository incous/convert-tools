import smtplib
from email.mime.text import MIMEText

mailserver = 'smtp.gmail.com'
username = ''
password = ''
mailfrom = ''
mailto = ''

msg = MIMEText("Hello world 2!")
msg['From'] = 'Sender <%s>' % mailfrom
msg['To'] = 'Receiver <%s>' % mailto
msg['Subject'] = 'Email subject here'

server = smtplib.SMTP(mailserver, 587)
# server.set_debuglevel(1)
server.ehlo()
server.starttls()
server.login(username, password)
server.sendmail(mailfrom, mailto, msg.as_string())
server.quit()
