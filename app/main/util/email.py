import smtplib
from email.message import EmailMessage
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import random
import string
EMAIL_ADDRESS = 'tryrenta@gmail.com'
EMAIL_PASSWORD = 'vgnpapuiolnsgtoi'

def send_confirmation_email(email, confirmation_token):
	text='''Please confirm your email ID at this link. http://localhost:3000/reset-password?token='''+confirmation_token
	html_text='''Please confirm your email ID at this link. <a href="http://localhost:3000/reset-password?token='''+confirmation_token+'''>Confirmation Link</a>'''
	#THIS LINK WILL CALL the <confirm/token> endpoint controller. You can enter your password here.
	html="""\
		<html>
		<body><p>"""+html_text+"""</p></body></html>"""
	message = MIMEMultipart("alternative")
	message["Subject"] = "Lasso: Change Password"
	message["From"] = EMAIL_ADDRESS
	message["To"] = email
	part1 = MIMEText(text, "plain")
	part2 = MIMEText(html, "html")
	message.attach(part1)
	message.attach(part2)
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
	    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD) 
	    smtp.sendmail(EMAIL_ADDRESS, email, message.as_string())

def set_password():
	x = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
	return x

def send_change_password_email(email, password):
	message = MIMEMultipart("alternative")
	message["Subject"] = "Lasso: Change Password"
	message["From"] = EMAIL_ADDRESS
	message["To"] = email
	text = '''Hello, we have received a request from your email account to change your password.
	Your new password is <b>'''+password+'''</b>. Please login using your new password. If this was not you, you can update to your old password once you login.'''
	html = """\
		<html>
		<body><p>"""+text+"""</p></body></html>"""
	part1 = MIMEText(text, "plain")
	part2 = MIMEText(html, "html")
	message.attach(part1)
	message.attach(part2)
	context = ssl.create_default_context()
	with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
	    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD) 
	    smtp.sendmail(EMAIL_ADDRESS, email, message.as_string())
