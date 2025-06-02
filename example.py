from flask import Flask, request, make_response, render_template

app = Flask(__name__)

@app.route('/')
def home():
	resposta = make_response('homepage.html')
	resposta.set_cookie('user', 'sala-1c')
	return render_template(resposta, page_title='home')

@app.route('/seecookie')
def cookies():
	cookies = request.cookies
	user = cookies.get('user')
	return user

app.run(debug=True)
