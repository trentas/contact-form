#!/usr/bin/python
# -*- coding: utf-8 -*-

from bottle import get, post, request, run, static_file, redirect, abort
import ConfigParser
import smtplib
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
import mimetypes
import codecs

CONFIG_FILE = '/etc/contact-form/contact-form.conf'

config = ConfigParser.ConfigParser()
config.read(CONFIG_FILE)
bind_address = config.get('main', 'bind_address')
bind_port = config.get('main', 'bind_port')
app_uri = config.get('main', 'app_uri')
static_document_root = config.get('main', 'static_document_root')

def send_email(smtp_server, smtp_port, smtp_tls, smtp_login, smtp_password, mail_from, receipt_to, msg):
	try:
		mail_sender = smtplib.SMTP(smtp_server, smtp_port)
		if smtp_tls:
			mail_sender.starttls()
		
		mail_sender.login(smtp_login, smtp_password)
		mail_sender.sendmail(mail_from, receipt_to, msg.as_string())
		mail_sender.close()
	except:
		raise

@get('/')
@get('%s/:destination' % (app_uri))
def server_file(destination='dummy'):
    return static_file(filename="index.html", root=static_document_root)

@post('%s/:destination' % (app_uri))
def send_form(destination):
	smtp_server = config.get(destination, 'smtp_server')
	smtp_port = config.get(destination, 'smtp_port')
	smtp_tls = config.get(destination, 'smtp_tls')
	smtp_login = config.get(destination, 'smtp_login')
	smtp_password = config.get(destination, 'smtp_password')
	receipt_to = config.get(destination, 'receipt_to')
	custom_subject_header = config.get(destination, 'custom_subject_header')
	redirect_after_success = config.get(destination, 'redirect_after_success')
	confirmation_email_template = config.get(destination, 'confirmation_email_template')
	custom_confirmation_subject = config.get(destination, 'custom_confirmation_subject')
	custom_file_request_notice = config.get(destination, 'custom_file_request_notice')
	file_to_send = config.get(destination, 'file_to_send')
	
	form_name = request.forms.get('name')
	form_email = request.forms.get('email')
	form_subject = request.forms.get('subject')
	form_body = request.forms.get('comments')
	form_sendfile = request.forms.get('sendfile')
	mail_from = '%s <%s>' % (form_name, form_email)
	subject = '%s %s' % (custom_subject_header, form_subject)
	if form_sendfile and file_to_send:
		form_body += '\n%s\n' % (custom_file_request_notice)
	
	msg = MIMEText(form_body)
	msg['From'] = mail_from
	msg['Reply-To'] = mail_from
	msg['To'] = receipt_to
	msg['Subject'] = Header(subject, 'utf-8')
	
	try:
		send_email(smtp_server, smtp_port, smtp_tls, smtp_login, smtp_password, mail_from, receipt_to, msg)
		if confirmation_email_template:
			email_template = codecs.open('%s/%s/%s' % (static_document_root, destination, confirmation_email_template), 'r', 'utf-8')
			confirmation_msg = MIMEMultipart('alternative')
			part1 = MIMEText(email_template.read(), 'html', 'utf-8')
			confirmation_msg.attach(part1)
			email_template.close()
			
			if file_to_send and form_sendfile:
				attachment_name = '%s/%s/%s' % (static_document_root, destination, file_to_send)
				ctype, encoding = mimetypes.guess_type(attachment_name)
				attachment = open(attachment_name, 'r')
				if ctype is None or encoding is not None:
					ctype = 'application/octet-stream'
				maintype, subtype = ctype.split('/', 1)
				if maintype == 'text':
					part2 = MIMEText(attachment.read(), _subtype=subtype)
				elif maintype == 'image':
					part2 = MIMEImage(attachment.read(), _subtype=subtype)
				elif maintype == 'audio':
					part2 = MIMEAudio(attachment.read(), _subtype=subtype)
				else:
					part2 = MIMEApplication(attachment.read(), _subtype=subtype)
				part2.add_header('Content-Disposition', 'attachment', filename=file_to_send)
				confirmation_msg.attach(part2)
				attachment.close()
			
			confirmation_msg['From'] = mail_from
			confirmation_msg['Reply-To'] = mail_from
			confirmation_msg['To'] = mail_from
			confirmation_msg['Subject'] = Header(custom_confirmation_subject, 'utf-8')
			send_email(smtp_server, smtp_port, smtp_tls, smtp_login, smtp_password, receipt_to, mail_from, confirmation_msg)
		
		redirect(redirect_after_success)
	except:
		raise
		#abort(500, "Error connecting to smtp server.")

run(host=bind_address, port=bind_port)

