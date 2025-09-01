from datetime import datetime
from DBcm import UseDatabase
import hashlib
import pytz

class SchoolData():
	def __init__(self, dbconfig):
		self.dbconfig = dbconfig

	def salas(codigo):
		match codigo:
			case 'tbmb1b':
				return '1a'
			case 'tbmb1c':
				return '1b'
			case 'tbmb1d':
				return '1c'
			case 'ucnc2c':
				return '2a'
			case 'ucnc2d':
				return '2b'
			case 'ucnc2e':
				return '2c'
			case 'vdod3d':
				return '3a'
			case 'vdod3e':
				return '3b'
			case 'vdod3f':
				return '3c'

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
		""" aulas dict
			sala -> dia -> aula -> (matéria, professor) """
		self.get_time()
		horario = self.horario()
		if horario in ('11', '12', '13', '0'):
			return ('Nada','Nenhum')
		if self.dia in ('Saturday', 'Sunday'):
			return ('Nada', 'Nenhum')
		with UseDatabase(self.dbconfig) as cursor:
			sql = '''select materia, prof from aulas
			where dia = %s and sala = %s and horario = %s'''
			cursor.execute(sql, (self.dia, sala, horario))
			results = cursor.fetchone()
		return results

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
