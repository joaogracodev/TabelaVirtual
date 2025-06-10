from flask import Flask, render_template, request, session, redirect, make_response
from schoollib import SchoolData

app = Flask(__name__)

if __name__ == '__main__':
	app.config['dbconfig'] = {'host' : 'localhost',
                        'user' : 'root',
			'password' : '',
			'database' : 'Tabela'}
else:
	app.config['dbconfig'] = {'host' : 'joaograco.mysql.pythonanywhere-services.com',
                                         'user' : 'joaograco',
                                         'password' : '3248213379a',
                                         'database' : 'joaograco$website'}

backend = SchoolData(app.config['dbconfig'])

@app.route('/logout')
def do_logout() -> str:
	if 'turma' in session:
		response = make_response('deslogado')
		session.pop('turma')
		cock = response.set_cookie('user', '', max_age=0)
	return response

@app.route('/login/err')
def login_error():
	if 'turma' in session:
		return redirect('/')
	title = 'Login'
	return render_template('login_error.html',
				page_title=title,)

@app.route('/login/')
def login():
	if 'turma' in session:
		return redirect('/')
	title = 'Login'
	if 'login_error' in session:
		print('login_error')
		return redirect('/login/err')
	return render_template('login.html',
				page_title=title,)

@app.route('/login/processing', methods=['POST'])
def prologin() -> 'html':
	turma = request.form['user']
	senha = request.form['password']
	proc = backend.login(turma.lower(), senha.lower())
	if proc['login'] == True:
		session['turma'] = proc['turma']
		response = make_response(redirect('/'))
		turma_cock = response.set_cookie('user', proc['turma'])
		if 'login_error' in session:
			session.pop('login_error')
	else:
		session['login_error'] = True
		return redirect('/login')
	return response

@app.route('/')
def init():
	cock = request.cookies
	if 'user' in cock:
		print('cock detected')
		session['turma'] = cock.get('user')
	return redirect('/homepage')

@app.route('/homepage')
def homepage():
	return render_template('homepage.html',
				page_title='Página Inicial',)

@app.route('/horario')
def horario() -> 'html':
	if 'turma' not in session:
		return redirect('/login')
	horario = backend.aula(session['turma'])
	print(horario)
	prof = horario[1]
	aula = horario[0]
	if aula != 'Nada':
		main_text = f'Agora está tendo aula de {aula}, com o professor(a) {prof}.'
	else:
		main_text = 'Agora não está tendo aula.'
	return render_template('horario.html',
				text=main_text,
				page_title='Horário da aula',)

@app.route('/almoco')
def almoco():
	if 'turma' not in session:
		return redirect('/login')
	raw_data = backend.almoco(session['turma'])
	ordem = raw_data['ordem']
	pos = raw_data['pos_sala']
	match pos:
		case 1:
			message = 'Sim, porque sua turma está em 1° lugar na fila do almoço.'
		case 2:
			message = 'Nem Tanto, porque sua turma estâ no 2° lugar na fila do almoço.'
		case 3:
			message = 'Não, porque sua turma está no 3° lugar da fila do almoço.'
	return render_template('almoco.html',
				message=message,
				first_class=ordem[0],
				second_class=ordem[1],
				third_class=ordem[2],)

app.secret_key = 'CentroDeExecelenciaDeEducacaoProfissionalJoseFigueredoBarreto'

if __name__ == '__main__':
	app.run(debug=True)
