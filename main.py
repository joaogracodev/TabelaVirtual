from flask import Flask, render_template, request, session, redirect, make_response, url_for
from schoollib import SchoolData
from html import escape
from DBcm import UseDatabase
import hashlib

app = Flask(__name__, static_folder='static')

if __name__ == '__main__':
	app.config['dbconfig'] = {'host' : 'localhost',
                        	  'user' : 'webDB',
							  'password' : 'DBpasswd',
							  'database' : 'Tabela'}
else:
	app.config['dbconfig'] = {'host' : 'joaograco.mysql.pythonanywhere-services.com',
                              'user' : 'joaograco',
                              'password' : '3248213379a',
                              'database' : 'joaograco$website'}

backend = SchoolData(app.config['dbconfig'])

@app.errorhandler(404)
def error_not_foun(error):
	return render_template('error.html', error_code=error, title='Insira um nome aqui'), 404

@app.route('/logout')
def do_logout() -> str:
	if 'turma' in session:
		response = make_response('deslogado')
		session.pop('turma')
		cock = response.set_cookie('user', '', max_age=0)
	return response

@app.route('/login/err')
def login_error():
	if 'login' in session:
		return redirect('/homepage')
	title = 'Login'
	return render_template('login_error.html',
				page_title=title,)

@app.route('/login/')
def login():
	if 'login' in session:
		return redirect('/homepage')
	title = 'Login'
	if 'login_error' in session:
		print('login_error')
		return redirect('/login/err')
	return render_template('login.html',
				page_title=title,)

@app.route('/login/continue/', methods=['POST'])
def login1():
	if 'login' in session:
		return redirect('/homepage')
	title = 'Login'
	email = request.form['email']
	with UseDatabase(app.config['dbconfig']) as cursor:
		sql = ''' select nome, id from users
  				where email = %s'''
		cursor.execute(sql, (email,))
		result = cursor.fetchone()
		if result == None:
			session['email_temp'] = email
			return redirect('/login/continue/create')
		nome = result[0]
	return render_template('login_part2.html',
				page_title=title, nome=nome)
 
@app.route('/login/continue/create')
def create_login():
	if 'login' in session:
		return redirect('/homepage')
	titulo = 'Criar conta'
	return render_template('login_create.html', title=titulo)

@app.route('/login/processing/<tipo>', methods=['POST'])
def prologin(tipo) -> 'html':
	if 'login' in session:
		return redirect('/homepage')
	def conta_existente(email, passwd):
		passwd_hash = hashlib.sha256(passwd.encode()).hexdigest()
		with UseDatabase(app.config['dbconfig']) as cursor:
			sql = '''select user, nome, email, sala, tipo from users where email=%s and senha=%s'''
			cursor.execute(sql, (email, passwd_hash))
			result = cursor.fetchone()
			if result == None:
				session['login_error'] = True
				return redirect('/login_error')
			return result
	def conta_inexistente(email, passwd, nome, sala_code, user) -> dict:
		passwd_hash = hashlib.sha256(passwd.encode()).hexdigest()
		with UseDatabase(app.config['dbconfig']) as cursor:
			sql = '''insert into users
					('user', 'nome', 'email', 'senha', 'sala', 'tipo')
   					values
					(%s, %s, %s, %s, %s, 'aluno')
       				'''
			cursor.execute(sql, (user, nome, email, passwd_hash, backend.salas(sala_code)))
			return None
	if tipo == 'login':
		batata = conta_existente(session['email_temp'], request.form['password'])
	elif tipo == 'create':
		batata = conta_inexistente()
	# salva dados
	minhajeba = make_response(redirect('/homepage'))
	# user_cookies = minhajeba.set_cookie('user_dict', batata)
	session['user'] = batata[0]
	session['sala'] = batata[3]
	session['tipo'] = batata[4]
	session['login'] = True
	if 'login_error' in session:
		session.pop('login_error')
	return redirect('/')

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
	if 'login' not in session:
		return redirect('/login/')
	horario = backend.aula(session['turma'])
	print(horario)
	prof = horario[1]
	aula = horario[0]
	if aula != 'Nada':
		main_text = escape(f'Agora está tendo aula de {aula}, com o professor(a) {prof}.')
	else:
		main_text = 'Agora não está tendo aula.'
	return render_template('horario.html',
				text=main_text,
				page_title='Horário da aula',)

@app.route('/almoco')
def almoco():
	"""_summary_

	Returns:
		_type_: _description_
	"""
	if 'turma' not in session:
		return redirect('/login')
	raw_data = backend.almoco(session['turma'])
	ordem = raw_data['ordem']
	pos = raw_data['pos_sala']
	match pos:
		case 1:
			message = escape('Sim, porque sua turma está em 1° lugar na fila do almoço.')
		case 2:
			message = escape('Nem Tanto, porque sua turma estâ no 2° lugar na fila do almoço.')
		case 3:
			message = escape('Não, porque sua turma está no 3° lugar da fila do almoço.')
	return render_template('almoco.html',
				message=message,
				first_class=ordem[0],
				second_class=ordem[1],
				third_class=ordem[2],)

app.secret_key = 'CentroDeExecelenciaDeEducacaoProfissionalJoseFigueredoBarreto'

if __name__ == '__main__':
	app.run(debug=True)
