from DBcm import UseDatabase

dbconfig = {'host' : 'localhost',
            'user' : 'root',
			'password' : '',
			'database' : 'Tabela'}
print(dbconfig)
with UseDatabase(dbconfig) as cursor:
    sql = '''select sala from users
    where id = %s'''
    print(sql)
    cursor.execute(sql, ('2',))
    result = cursor.fetchone()
    print(result)
print(result)
