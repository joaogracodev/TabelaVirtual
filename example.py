from DBcm import UseDatabase
import hashlib

def cripto(passwd):
	hash_obj = hashlib.sha256(passwd.encode())
	return hash_obj.hexdigest()

dbconfig = {'host' : 'joaograco.mysql.pythonanywhere-services.com',
                                         'user' : 'joaograco',
                                         'password' : '3248213379a',
                                         'database' : 'joaograco$website'}

with UseDatabase(dbconfig) as cursor:
	sql = """insert into users
		(user, password, sala)
		 values
		(%s, %s, %s)"""
	usrs = [('sala-1a', cripto('tbmb1b'), '1a'), ('sala-1b', cripto('tbmb1c'), '1b'), ('sala-1c', cripto('tbmb1d'), '1c'), ('sala-2a', cripto('ucnc2c'), '2a'), ('sala-2b', cripto('ucnc2d'), '2b'), ('sala-2c', cripto('ucnc2e'), '2c'), ('sala-3a', cripto('vdod3d'), '3a'), ('sala-3b', cripto('vdod3e'), '3b'), ('sala-3c', cripto('vdod3f'), '3c')]
	for usr in usrs:
		cursor.execute(sql, (usr[0], usr[1], usr[2]))

