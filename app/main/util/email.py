import smtplib
from email.message import EmailMessage
import random
import string

def set_password():
	x = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
	return x

def send_email(email, password):
	#TO DO NEED TO SETUP EMAIL FUNCTION
	EMAIL_ADDRESS = 'your_email_address'
	EMAIL_PASSWORD = 'your_app_password'

	msg = EmailMessage()
	msg['Subject'] = 'This is my first Python email'
	msg['From'] = EMAIL_ADDRESS 
	msg['To'] = email
	msg.set_content('Hello your prior password was $this. Your new password is $this. Please change it')


	with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
	    smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD) 
	    smtp.send_message(msg)


