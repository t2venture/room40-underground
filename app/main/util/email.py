import smtplib
from email.message import EmailMessage
import random
import string
EMAIL_ADDRESS = 'tryrenta@gmail.com'
EMAIL_PASSWORD = 'vgnpapuiolnsgtoi'
def set_password():
	x = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
	return x

def send_email(email, password):

	msg = EmailMessage()
	msg['Subject'] = 'Lasso: Password Change Request'
	msg['From'] = EMAIL_ADDRESS 
	msg['To'] = email
	content='''Hello, we have received a request from your email account to change your password.
	Your new password is '''+password+'''. Please login using your new password.'''
	msg.set_content()


	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
	    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD) 
	    smtp.send_message(msg)
