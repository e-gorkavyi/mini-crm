import mysql.connector as mc
from mysql.connector import errorcode
from PyQt5 import QtWidgets

def create_connection(host_name, port_number, db_name, user_name, user_password):
	msgBox = QtWidgets.QMessageBox()
	connection = None
	try:
		connection = mc.connect(
			host=host_name,
			port=port_number,
			user=user_name,
			password=user_password,
			database=db_name,
			ssl_ca='mysql_ssl\\ca.pem',
			ssl_key='mysql_ssl\\client-key.pem',
			ssl_cert='mysql_ssl\\client-cert.pem'
		)
	except mc.Error as e:
		if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
			msg = 'Неверный логин или пароль'
		elif e.errno == errorcode.ER_BAD_DB_ERROR:
			msg = 'База данных не найдена на сервере'
		else:
			msg = 'Соединение невозможно'
		msgBox.setWindowTitle('Ошибка подключения')
		msgBox.setText(msg)
		msgBox.exec()
	return connection

def database_query(self, connection, query):
	cursor = connection.cursor()
	try:
		cursor.execute(query)
		return cursor
	except mc.Error:
		return False