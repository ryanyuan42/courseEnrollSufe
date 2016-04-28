from email.header    import Header
from email.mime.text import MIMEText
from getpass         import getpass
from smtplib         import SMTP_SSL

class Sender:
	def __init__(self, username, pwd):
		self.login, self.password = username, pwd

	def createMsg(self, body, subject, From = yourEmailAddress, To = receiverEmailAddress):
		self.msg = MIMEText(body, _charset='utf-8')
		self.msg['Subject'] = Header(subject, 'utf-8')
		self.msg['From'] = From
		self.msg['To'] = To
	def sendmail(self):
		# create message
		# send it via gmail
		s = SMTP_SSL('smtp.gmail.com', 465, timeout=10)
		s.set_debuglevel(1)
		try:
		    s.login(self.login, self.password)
		    s.sendmail(self.msg['From'], self.msg['To'],self. msg.as_string())
		finally:
		    s.quit()

