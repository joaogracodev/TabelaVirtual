from datetime import datetime
from DBcm import UseDatabase
import hashlib
import pytz

class SchoolData():
	def __init__(self, dbconfig):
		self.dbconfig = dbconfig

	def login(self, user, passwd) -> dict:
		hash_obj = hashlib.sha256(passwd.encode())
		passwd_hash = hash_obj.hexdigest()
		with UseDatabase(self.dbconfig) as cursor:
			sql = '''select user, password, sala from users'''
			cursor.execute(sql)
			results = cursor.fetchall()
		for line in results:
			if user in line[0] and passwd_hash == line[1]:
				return {'login' : True, 'turma' : line[2]}
		return {'login' : False, 'turma' : ''}

	def get_time(self):
		timezone = pytz.timezone('America/Sao_Paulo')
		self.agora = datetime.now(timezone)
		self.dia = self.agora.strftime('%A')
		self.hora = int(self.agora.strftime('%H'))
		self.data = self.agora.day
		self.minuto = int(self.agora.strftime('%M'))

	def horario(self):
		""" 11 = lanche manha
	    	12 = aumoço
   		13 = lanche tarde """
		agora = '0'
		self.get_time()
		match self.hora:
			case 7:
				if self.minuto in list(range(50, 59, 1)):
					agora = '2'
				elif self.minuto in list(range(0, 49, 1)):
					agora = '1'
			case 8:
				if self.minuto in list(range(0, 40, 1)):
					agora = '2'
				elif self.minuto in list(range(39, 59, 1)):
					agora = '3'
			case 9:
				if self.minuto in list(range(0, 29, 1)):
					agora = '3'
				elif self.minuto in list(range(30, 49, 1)):
					agora = '11'
				elif self.minuto in list(range(50, 59, 1)):
					agora = '4'
			case 10:
				if self.minuto in list(range(0, 39, 1)):
					agora = '4'
				elif self.minuto in list(range(40, 59, 1)):
					agora = '5'
			case 11:
				if self.minuto in list(range(0, 29, 1)):
					agora = '5'
				if self.minuto in list(range(30, 59, 1)):
					agora = '12'
			case 12:
				if self.minuto in list(range(0, 59, 1)):
					agora = '12'
			case 13:
				if self.minuto in list(range(0, 49, 1)):
					agora = '6'
				if self.minuto in list(range(50, 59, 1)):
					agora = '7'
			case 14:
				if self.minuto in list(range(0, 39, 1)):
					agora = '7'
				if self.minuto in list(range(40, 49, 1)):
					agora = '13'
				if self.minuto in list(range(50, 59, 1)):
					agora = '8'
			case 15:
				if self.minuto in list(range(0, 39, 1)):
					agora = '8'
				if self.minuto in list(range(40, 59, 1)):
					agora = '9'
			case 16:
				if self.minuto in list(range(0, 29, 1)):
					agora = '9'
			case _:
				agora = '0'
		return agora

	def aula(self, sala):
		sem_prof = 'Sem Professor'
		""" aulas dict
			sala -> dia -> aula -> (matéria, professor) """
		self.get_time()
		horario = self.horario()
		if horario in ('11', '12', '13', '0'):
			return ('Nada','Nenhum')
		if self.dia in ('Saturday', 'Sunday'):
			return ('Nada'  'Nenhum')
		aulas = {
		'1a' : {
			'Monday' : {
				'1' : ('Química', 'Adriana'),
				'2' : ('Português', 'Victor'),
				'3' : ('Biologia', 'Karla'),
				'4' : ('Estudo Orientado', 'Joanelice'),
				'5' : ('Língua Portuguesa', 'Victor'),
				'6' : ('Geografia', 'Edilson Carneiro'),
				'7' : ('Ecologia e Meio Ambiente', 'Kalideri'),
				'8' : ('Educação Física', 'David'),
				'9' : ('Esporte, Cultura e Arte na Prática', 'David')},
			'Tuesday' : {
				'1' : ('Lingua Inglesa', 'Ricleberson'),
				'2' : ('Matemática', 'Jussara Abreu'),
				'3' : ('Filosofia', sem_prof),
				'4' : ('Sociologia', 'Claudia'),
				'5' : ('Redação', 'Carla'),
				'6' : ('Eletivas', 'Vários professores'),
				'7' : ('Eletivas', 'Vários professores'),
				'8' : ('Projeto de Vida', 'Karla'),
				'9' : ('Projeto de Vida', 'Karla')},
			'Wednesday' : {
				'1' : ('História, Cultura e Identidades Sergipanas', 'Joanelice'),
				'2' : ('Filosofia', sem_prof),
				'3' : ('História', 'Joanelice'),
				'4' : ('Estudo Orientado', 'Joanelice'),
				'5' : ('Operações Matemáticas', 'Jussara Abreu'),
				'6' : ('Educação Física', 'David'),
				'7' : ('Artes', 'Luciana'),
				'8' : ('Tutoria', 'Claudia'),
				'9' : ('Esporte, Cultura e Arte na Prática', 'David')},
			'Thursday' : {
				'1' : ('Língua Portuguesa', 'Victor'),
				'2' : ('Redação', 'Carla'),
				'3' : ('Física', 'Mário'),
				'4' : ('Sociologia', 'Claudia'),
				'5' : ('História', 'Joanelice'),
				'6' : ('Ecologia e Meio Ambiente', 'Kalideri'),
				'7' : ('Matemática', 'Jussara Abreu'),
				'8' : ('Geografia', 'Edilson Carneiro'),
				'9' : ('Física', 'Mário')},
			'Friday': {
				'1' : ('Língua Portuguesa', 'Victor'),
				'2' : ('Química', 'Adriana'),
				'3' : ('Artes', 'Luciana'),
				'4' : ('Estudo Orientado', 'Joanelice'),
				'5' : ('Biologia', 'Karla'),
				'6' : ('Operações Matemáticas', 'Jussara Abreu'),
				'7' : ('Matemática', 'Jussara Abreu'),
				'8' : ('Língua Inglesa', 'Ricleberson'),
				'9' : ('História, Cultura e Identidades Sergipanas', 'Joanelice')}},
		'1b' : {
			'Monday' : {
				'1' : ('História', 'Joanelice'),
				'2' : ('História, Cultura e Identidades Sergipanas', 'Joanelice'),
				'3' : ('Língua Portuguesa', 'Victor'),
				'4' : ('Matemática', 'Jussara'),
				'5' : ('Geografia', 'Edilson Carneiro'),
				'6' : ('Química', 'Adriana'),
				'7' : ('Estudo Orientado', 'Adriana'),
				'8' : ('Biologia', 'Karla'),
				'9' : ('Geografia', 'Edilson')},
			'Tuesday' : {
				'1' : ('Ecologia e Meio Ambiente', 'Kalideri'),
				'2' : ('Língua Inglesa', 'Ricleberson'),
				'3' : ('Sociologia', 'Claudia'),
				'4' : ('Filosofia', sem_prof),
				'5' : ('Estudo Orientado', 'Adriana'),
				'6' : ('Eletivas', 'Vários Professores'),
				'7' : ('Eletivas', 'Vários Professores'),
				'8' : ('Língua Portuguesa', 'Victor'),
				'9' : ('Operações Matemáticas', 'Jussara Abreu')},
			'Wednesday' : {
				'1' : ('Educação Física', 'David'),
				'2' : ('Redação', 'Carla'),
				'3' : ('Filosofia', sem_prof),
				'4' : ('Educação Física', 'David'),
				'5' : ('Esporte, Arte e Cultura na Prática', 'David'),
				'6' : ('Projeto de Vida', 'Karla'),
				'7' : ('Projeto de Vida', 'Karla'),
				'8' : ('Tutoria', 'David'),
				'9' : ('Ecologia e Meio Ambiente', 'Kalideri')},
			'Thursday' : {
				'1' : ('Física', 'Mário'),
				'2' : ('Matemática', 'Jussara Abreu'),
				'3' : ('Língua Portuguesa', 'Victor'),
				'4' : ('Estudo Orientado', 'Adriana'),
				'5' : ('Química', 'Adriana'),
				'6' : ('Operações Matemáticas', 'Jussara Abreu'),
				'7' : ('Artes', 'Luciana'),
				'8' : ('História', 'Joanelice'),
				'9' : ('Língua Inglesa', 'Joanelice')},
			'Friday' : {
				'1' : ('Matemática', 'Jussara Abreu'),
				'2' : ('Física', 'Mário'),
				'3' : ('Redação', 'Carla'),
				'4' : ('Esporte, Cultura e Arte na Prática', 'David'),
				'5' : ('Artes', 'Luciana'),
				'6' : ('Língua Portuguesa', 'Victor'),
				'7' : ('Biologia', 'Karla'),
				'8' : ('História, Cultura e Identidades Sergipanas', 'Joanelice'),
				'9' : ('Sociologia', 'Claudia')}},

		'1c' : {
			'Monday' : {
				'1' : ('Lingua Portuguesa', 'Victor'),
				'2' : ('Estudo Orientado', 'Edilson Carneiro'),
				'3' : ('Matemática', 'Jussara'),
				'4' : ('Lingua Portuguesa', 'Vitor'),
				'5' : ('História', 'Joanelice'),
				'6' : ('Biologia', 'Karla'),
				'7' : ('Educação Física', 'David'),
				'8' : ('Geografia', 'Edilson Carneiro'),
				'9' : ('Redação', 'Carla')},
			'Tuesday' : {
				'1' : ('Operações Matemáticas', 'Jussara Abreu'),
				'2' : ('Química', 'Adriana'),
				'3' : ('Artes', 'Luciana'),
				'4' : ('Matemática', 'Jussara Abreu'),
				'5' : ('Ecologia e Meio-Ambiente', 'Kalideri'),
				'6' : ('Eletiva', 'Vários'),
				'7' : ('Eletiva', 'Vários'),
				'8' : ('Sociologia', 'Claudia'),
				'9' : ('Esporte, Arte e Cultura na Prática', 'David')},
			'Wednesday' : {
				'1' : ('Filosofia', sem_prof),
				'2' : ('Projeto de Vida', 'Karla'),
				'3' : ('Projeto de Vida', 'Karla'),
				'4' : ('Operações Matemáticas', 'Jussara Abreu'),
				'5' : ('Filosofia', sem_prof),
				'6' : ('Física', 'Mário César'),
				'7' : ('Educação Física', 'David'),
				'8' : ('Tutoria', 'Edilson Carneiro'),
				'9' : ('Historia, Cultura e Identidades Sergipanas', 'Joanelice')},
			'Thursday' : {
				'1' : ('Química', 'Adriana'),
				'2' : ('Física', 'Mário'),
				'3' : ('Lingua Inglesa', 'Ricleberson'),
				'4' : ('Redação', 'Carla'),
				'5' : ('Sociologia', 'Claudia'),
				'6' : ('Artes', 'Luciana'),
				'7' : ('História', 'Joanelice'),
				'8' : ('Matemática', 'Jussara'),
				'9' : ('Estudo Orientado', 'Edilson Carneiro')},
			'Friday' : {
				'1' : ('Esporte, arte e cultura na Prática', 'David'),
				'2' : ('História, Cultura e Identidades Sergipanas', 'Joanelice'),
				'3' : ('Ecologia e Meio Ambiente', 'Kalideri'),
				'4' : ('Biologia', 'Karla'),
				'5' : ('Portugês', 'Vitor'),
				'6' : ('Lingua Inglesa', 'Ricleberson'),
				'7' : ('Português', 'Victor'),
				'8' : ('Estudo Orientado', 'Edilson Carneiro'),
				'9' : ('Geografia', 'Edilson Carneiro')}},}

		return aulas[sala][self.dia][horario]

	def almoco(self, turma):
		self.get_time()
		new_turma = list(turma).pop(0)
		if self.data in list(range(1, 31, 3)):
			ordem = '1|2|3'.split('|')
		elif self.data in list(range(2, 31, 3)):
			ordem = '3|1|2'.split('|')
		elif self.data in list(range(3, 31, 3)):
			ordem = '2|3|1'.split('|')
		return {'ordem' : ordem, 'pos_sala' : (ordem.index(new_turma)+1)}
