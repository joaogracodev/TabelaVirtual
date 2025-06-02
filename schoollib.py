from datetime import datetime

class SchoolData():
	def __init__(self):
		pass

	def login(self, user, passwd) -> tuple:
		match user:
			case 'sala-1c':
				if passwd == 'balacobaco':
					return (True, '1c')
			case 'sala-1a':
				if passwd == 'blackpink':
					return (True, '1c')
		return (False)
	def get_time(self):
		self.agora = datetime.now()
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
		if horario in ('11', '12', '13'):
			return ('Intervalo','Nenhum')
		if self.dia in ('Saturday', 'Sunday'):
			return ('Nada'  'Nenhum')
		if horario == '0':
			return ('Nada', 'Nenhum')
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
				'9' : ('Projeto de Vida', 'Karla')}
			'Wednesday' : {
				'1' : ('História, Cultura e Identidades Sergipanas', 'Joanelice'),
				'2' : ('Filosofia', sem_prof),
				'3' : ('História', 'Joanelice'),
				'4' : ('Estudo Orientado', 'Joanelice'),
				'5' : ('Operações Matemáticas', 'Jussara Abreu'),
				'6' : ('Educação Física', 'David'),
				}}

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
			ordem = ('1', '2', '3')
		elif self.data in list(range(2, 31, 3)):
			ordem = ('3', '1', '2')
		elif self.data in list(range(3, 31, 3)):
			ordem = ('2', '3', '1')
		return {'ordem' : ordem, 'pos_sala' : (ordem.index(new_turma)+1)}
