from bottle import get, post, request, run, static_file, redirect
import smtplib
from email.MIMEText import MIMEText

STATIC_ROOT_PATH = "static/"
BIND_ADDRESS = "localhost"
BIND_PORT = "8080"

MAIL_RECIPIENT = 'my_dest_email@gmail.com'
REDIRECT_AFTER_SUCESS = 'http://google.com/'

GMAIL_LOGIN = 'my_gmail_login@gmail.com'
GMAIL_PASSWORD = 'my_gmail_password'

@get('/')
@get('/contact/:destination')
def server_file(destination='dummy'):
    return static_file(filename="index.html", root=STATIC_ROOT_PATH)

@post('/contact/:destination')
def send_form(destination):
	form_name = request.forms.get('name')
	form_email = request.forms.get('email')
	form_subject = request.forms.get('subject')
	form_body = request.forms.get('comments')
	mail_from = '%s <%s>' % (form_name, form_email)
	rcpt_to = MAIL_RECIPIENT
	msg = MIMEText(form_body)
	msg['From'] = mail_from
	msg['Reply-To'] = mail_from
	msg['To'] = rcpt_to
	msg['Subject'] = form_subject
	try:
		smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
		smtp_server.starttls()
		smtp_server.login(GMAIL_LOGIN, GMAIL_PASSWORD)
		smtp_server.sendmail(mail_from, MAIL_RECIPIENT, msg.as_string())
		smtp_server.close()
		redirect(REDIRECT_AFTER_SUCESS)
	except:
		#raise
		return "Error connecting to smtp server"


run(host=BIND_ADDRESS, port=BIND_PORT)

