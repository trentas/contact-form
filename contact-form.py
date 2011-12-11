from bottle import get, post, route, request, run, static_file

STATIC_ROOT_PATH = "static/"

#@route('/contact/')
@get('/contact/:destination')
def server_file(destination='bond'):
    return static_file(filename="index.html", root=STATIC_ROOT_PATH)

@post('/contact/:destination')
def send_form(destination):
	name = request.forms.get('name')
	email = request.forms.get('email')
	comments = request.forms.get('comments')
	return 'Nome: %s, Email: %s, Comentarios:%s, Cliente:%s' % (name, email, comments, destination)

run(host='10.211.55.4', port=8080)

