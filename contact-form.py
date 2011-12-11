from bottle import get, post, request, run, static_file, redirect, abort
import ConfigParser
import smtplib
from email.MIMEText import MIMEText

CONFIG_FILE = 'contact-form.conf'

config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)
bind_address = config.get('main', 'bind_address')
bind_port = config.get('main', 'bind_port')
static_document_root = config.get('main', 'static_document_root')

@get('/')
@get('/contact/:destination')
def server_file(destination='dummy'):
    return static_file(filename="index.html", root=static_document_root)

@post('/contact/:destination')
def send_form(destination):
	gmail_login = config.get(destination, 'gmail_login')
	gmail_password = config.get(destination, 'gmail_password')
	gmail_rcpt_to = config.get(destination, 'gmail_rcpt_to')
	custom_subject_header = config.get(destination, 'custom_subject_header')
	redirect_after_sucess = config.get(destination, 'redirect_after_sucess')
	form_name = request.forms.get('name')
	form_email = request.forms.get('email')
	form_subject = request.forms.get('subject')
	form_body = request.forms.get('comments')
	mail_from = '%s <%s>' % (form_name, form_email)
	subject = '%s %s' % (custom_subject_header, form_subject)
	msg = MIMEText(form_body)
	msg['From'] = mail_from
	msg['Reply-To'] = mail_from
	msg['To'] = gmail_rcpt_to
	msg['Subject'] = subject
	try:
		smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
		smtp_server.starttls()
		smtp_server.login(gmail_login, gmail_password)
		smtp_server.sendmail(mail_from, gmail_rcpt_to, msg.as_string())
		smtp_server.close()
		redirect(redirect_after_sucess)
	except:
		raise
		#abort(500, "Error connecting to smtp server.")


run(host=bind_address, port=bind_port)

