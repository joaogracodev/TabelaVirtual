from flask import Flask, render_template, request, session, redirect, make_response, url_for
from schoollib import SchoolData
from html import escape
from DBcm import UseDatabase
import hashlib
from check import loggedin, loggedout

app = Flask(__name__, static_folder='static')

if __name__ == '__main__':
    app.config['dbconfig'] = {'host' : 'localhost', 'user' : 'webDB', 'password' : 'DBpasswd', 'database' : 'Tabela'}

else:
    app.config['dbconfig'] = {'host' : 'joaograco.mysql.pythonanywhere-services.com', 'user' : 'joaograco', 'password' : '3248213379a', 'database' : 'joaograco$website'}

mylib = SchoolData(app.config['dbconfig'])

@app.route('/')
def slash():
    cookies = request.cookies
    if 'user' in cookies:
        session['nome'] = cookies.get('nome')
        session['turma'] = cookies.get('turma')
    return redirect('/home')

@app.route('/home')
def home():
    titulo = escape('Página Inicial')
    return render_template('home.html', page_title=titulo), 200

@app.route('/aula')
@loggedin
def aula():
    titulo = 'Aula'
    aula_agora = mylib.aula(session['sala'])
    aula = aula_agora[0]
    prof = aula_agora[1]
    if aula != 'Nada':
        texto = escape(f'Agora está tendo aula de {aula}, com o professor(a) {prof}.')
    else:
        texto = escape('Agora não está tendo aula')
    return render_template('horario.html', text=texto, page_title=titulo)

@app.route('/almoco')
@loggedin
def almoco():
    titulo = 'Fila'
    dados = mylib.almoco(session['sala'])
    ordem = dados['ordem']
    posicao = dados['pos_sala']
    return render_template('almoco.html', page_title=titulo, my=posicao, serie1=ordem[0], serie2=ordem[1], serie3=ordem[2])

@app.route('/login/')
@loggedout
def login():
    titulo = 'Login'
    if 'login_error' in session:
        return redirect('/login/err')
    return render_template('login.html', page_title=titulo)

@app.route('/login/continue', methods=['POST'])
@loggedout
def login_continue():
    titulo = 'Login'
    temp_email = request.form['email']
    with UseDatabase(app.config['dbconfig']) as cursor:
        sql = '''select nome from users where email=%s'''
        cursor.execute(sql, (temp_email,))
        resultado = cursor.fetchone()
        session['temp_email'] = temp_email
        if resultado != None:
            return render_template('login_part2.html', page_title=titulo, nome=resultado[0])
        return redirect('/login/continue/criar')
    
@app.route('/login/enviando/<tipo>', methods=['POST'])
@loggedout
def login_enviando(tipo):
    match tipo:
        case 'login':
            senha = request.form['password']
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            email = session['temp_email']
            with UseDatabase(app.config['dbconfig']) as cursor:
                sql = '''select nome, sala, tipo from users where email=%s and senha=%s'''
                cursor.execute(sql, (email, senha_hash))
                resultado = cursor.fetchone()
                if resultado != None:
                    response = make_response(redirect('/'))
                    nome_cookie = response.set_cookie('nome', resultado[0])
                    session['nome'] = resultado[0]
                    sala_cookie = response.set_cookie('sala', resultado[1])
                    session['sala'] = resultado[1]
                    tipo_cookie = response.set_cookie('tipo', resultado[2])
                    session['tipo'] = resultado[2]
                    session['login'] = True
                    return response
                else:
                    return redirect('/login/contiune/err')
        case 'login_err':
            senha = request.form['password']
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()
            email = request.form['email']
            with UseDatabase(app.config['dbconfig']) as cursor:
                sql = '''select nome, sala, tipo from users where email=%s and senha=%s'''
                cursor.execute(sql, (email, senha_hash))
                resultado = cursor.fetchone()
                if resultado != None:
                    response = make_response(redirect('/'))
                    nome_cookie = response.set_cookie('nome', resultado[0])
                    session['nome'] = resultado[0]
                    sala_cookie = response.set_cookie('sala', resultado[1])
                    session['sala'] = resultado[1]
                    tipo_cookie = response.set_cookie('tipo', resultado[2])
                    session['tipo'] = resultado[2]
                    session['login'] = True
                    return response
        case 'criar':
            pass

@app.route('/logout')
@loggedin
def logout():
    response = make_response('<h1>deslogado</h1>')
    dados = ('nome', 'sala', 'tipo')
    for dado in dados:
        if dado in session:
            session.pop(dado)
        cookie = response.set_cookie(dado, '', max_age=0)
    session.pop('login')
    return response

@app.route('/login/continue/criar', methods=['POST', 'GET'])
def login_criar():
    email = escape(session['temp_email'])
    return render_template('login_criar.html', email=email)

@app.errorhandler(404)
def error(err):
    titulo = escape('Erro 404')
    return render_template('error.html', error_code=err, title=titulo, the_title=titulo)


app.secret_key = 'HatsuneMiku123'
if __name__ == '__main__':
    app.run(debug=True)