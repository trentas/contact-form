from bottle import get, post, run, static_file


STATIC_ROOT_PATH = "static/"
BIND_ADDRESS = "localhost"
BIND_PORT = "8080"

@get('/contact/:destination')
def server_file(destination='dummy'):
    return static_file(filename="index.html", root=STATIC_ROOT_PATH)

@post('/contact/:destination')
def send_form(destination):
	name = request.forms.get('name')
	email = request.forms.get('email')
	subject = request.forms.get('subject')
	comments = request.forms.get('comments')
	return 'Name: %s, Email: %s, Subject: %s, Comments:%s, Destination:%s' % (name, email, subject, comments, destination)

run(host=BIND_ADDRESS, port=BIND_PORT)

