import decimal, datetime, locale

try:
	locale.setlocale(locale.LC_ALL, '')
except:
	pass

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QEvent, QDate, QDateTime, Qt

import edit_pay
import main_form_concept, edit_project, edit_partner, settings_interface, login, directory_window, sys
import mysql.connector as mc
from mysql.connector import errorcode
from mysql.connector.locales.eng import client_error

QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)  # enable highdpi scaling
QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)  # use highdpi icons

loginInfo = {'host': '',
             'port': '',
             'db': '',
             'user': '',
             'pass': '',
             'id': '',
             'ssl': ''}

connection = None

def create_connection(silent = False):
	global connection
	msgBox = QtWidgets.QMessageBox()
	try:
		if not loginInfo['ssl']:
			connection = mc.connect(
				host=loginInfo.get('host'),
				port=loginInfo.get('port'),
				user=loginInfo.get('user'),
				password=loginInfo.get('pass'),
				database=loginInfo.get('db'),
				charset = 'utf8mb4',
			    collation = 'utf8mb4_unicode_ci',
				use_unicode = True
			)
		else:
			connection = mc.connect(
				host=loginInfo.get('host'),
				port=loginInfo.get('port'),
				user=loginInfo.get('user'),
				password=loginInfo.get('pass'),
				database=loginInfo.get('db'),
				ssl_ca = 'mysql_ssl\\ca.pem',
				ssl_key = 'mysql_ssl\\client-key.pem',
				ssl_cert = 'mysql_ssl\\client-cert.pem',
				charset = 'utf8mb4',
			    collation = 'utf8mb4_unicode_ci',
				use_unicode = True)
	except mc.Error as e:
		if not silent:
			if e.errno == errorcode.ER_ACCESS_DENIED_ERROR:
				msg = 'Неверный логин или пароль'
			elif e.errno == errorcode.ER_BAD_DB_ERROR:
				msg = 'База данных с таким именем не найдена на сервере'
			else:
				msg = 'Соединение невозможно. Код ошибки ' + str(e.errno)
			msgBox.setWindowTitle('Ошибка подключения')
			msgBox.setText(msg)
			msgBox.exec()
		return False
	return True

def recon():
	global connection
	try:
		connection.ping(reconnect=True, attempts=3, delay=5)
	except mc.Error as e:
		create_connection(True)

def query(query):
	global connection
	recon()
	cur = connection.cursor()
	cur.execute(query)
	result = cur.fetchall()
	connection.commit()
	return result


def queryOne(query):
	global connection
	recon()
	cur = connection.cursor()
	cur.execute(query)
	result = cur.fetchone()
	connection.commit()
	return result


def queryInsert(sql, data):
	global connection
	recon()
	cur = connection.cursor()
	cur.execute(sql, data)
	last_id = cur.lastrowid
	connection.commit()
	return last_id


def queryDB(sql, data):
	global connection
	recon()
	cur = connection.cursor()
	cur.execute(sql, data)
	result = cur.fetchall()
	connection.commit()
	return result

class DateTimeWidgetItem(QtWidgets.QTableWidgetItem):
	def __init__(self, text, sortKey):
		#call custom constructor with UserType item type
		QtWidgets.QTableWidgetItem.__init__(self, text, QtWidgets.QTableWidgetItem.UserType)
		self.sortKey = sortKey

	#Qt uses a simple < check for sorting items, override this to use the sortKey
	def __lt__(self, other):
		return self.sortKey < other.sortKey

class LoginDB(QtWidgets.QDialog, login.Ui_Dialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)

		self.settings = QtCore.QSettings('AcademUpack', 'ERP')
		self.hostEdit.setText(self.settings.value("DB_Host", ""))
		self.portEdit.setText(self.settings.value("DB_Port", ""))
		self.DBNameEdit.setText(self.settings.value("DB_Name", ""))
		self.sslCheckBox.setChecked(True)
		self.sslCheckBox.setChecked(True if self.settings.value("DB_ssl") == 'true' else False)

		fnt = QtGui.QFont()
		fnt.setPointSize(int(self.settings.value("font_size", 10)))
		self.setFont(fnt)

		self.hostEdit.textChanged.connect(self.saveState)
		self.portEdit.textChanged.connect(self.saveState)
		self.DBNameEdit.textChanged.connect(self.saveState)
		self.sslCheckBox.stateChanged.connect(self.saveState)
		self.pushButton.clicked.connect(self.database_connection)
		self.connection = None

	def database_connection(self):
		loginInfo['host'] = self.hostEdit.text()
		loginInfo['port'] = self.portEdit.text()
		loginInfo['db'] = self.DBNameEdit.text()
		loginInfo['user'] = self.loginEdit.text()
		loginInfo['pass'] = self.passEdit.text()
		loginInfo['ssl'] = self.sslCheckBox.isChecked()
		self.connection = create_connection()
		if self.connection:
			self.hide()

	def saveState(self):
		self.settings.setValue("DB_Host", self.hostEdit.text())
		self.settings.setValue("DB_Port", self.portEdit.text())
		self.settings.setValue("DB_Name", self.DBNameEdit.text())
		self.settings.setValue("DB_ssl", self.sslCheckBox.isChecked())

	def query(self, query):
		cursor = self.connection.cursor()
		cursor.execute(query)
		self.connection.commit()
		return cursor


class InterfaceSettings(QtWidgets.QDialog, settings_interface.Ui_Dialog):
	signalSpinChange = QtCore.pyqtSignal(int)
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)

		self.settings = QtCore.QSettings('AcademUpack', 'ERP')
		self.spinBox.setValue(int(self.settings.value("font_size", 10)))

		self.spinBox.valueChanged.connect(self.signalSpinChangeEmit)

		fnt = QtGui.QFont()
		fnt.setPointSize(int(self.settings.value("font_size", 10)))
		self.setFont(fnt)

	def signalSpinChangeEmit(self):
		self.signalSpinChange.emit(self.spinBox.value())
		self.settings.setValue("font_size", self.spinBox.value())


class DirectoryWindow(QtWidgets.QDialog, directory_window.Ui_DirectoryWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)
		self.settings = QtCore.QSettings('AcademUpack', 'ERP')
		self.filterButton.pressed.connect(self.tableFill)
		self.directoryTable.installEventFilter(self)
		self.tableName = ''

		fnt = QtGui.QFont()
		fnt.setPointSize(int(self.settings.value("font_size", 10)))
		self.setFont(fnt)
		self.directoryTable.setFont(fnt)

	def tableFill(self):
		self.resize(self.settings.value("directory_%s_window_size" % self.tableName, QtCore.QSize(300, 300)))
		self.move(self.settings.value("directory_%s_window_pos" % self.tableName, QtCore.QPoint(100, 100)))
		self.directoryTable.setSortingEnabled(False)
		while self.directoryTable.rowCount() > 0:
			self.directoryTable.removeRow(0)
		whereTxt = '1'
		if self.tableName == 'partners':
			try:
				self.directoryTable.disconnect()
			except Exception:
				pass
			self.directoryTable.doubleClicked['QModelIndex'].connect(self.editPartner)
			self.newButton.pressed.connect(self.newPartner)
			self.setWindowTitle('Список партнёров')
			self.directoryTable.setColumnCount(5)
			self.directoryTable.setHorizontalHeaderLabels(['id', 'Наименование', 'Город', 'Клиент', 'Поставщик'])
			for index in range(self.directoryTable.columnCount()):
				self.directoryTable.setColumnWidth(index, self.settings.value('directoryTableColW_%s_%s' % (index, self.tableName), 50))
			self.directoryTable.hideColumn(0)
			if self.lineEdit.text() != '':
				whereTxt += " and name LIKE '%%%s%%' or city LIKE '%%%s%%'" % (self.lineEdit.text(), self.lineEdit.text())
			rows = query('''
				select
					partners.id, partners.name, partners.city, if(partners.client = TRUE, '+', '-'), if(partners.seller = TRUE, '+', '-')
				from partners
				where %s  
				order by name
			''' % whereTxt)
			for row_number, row_data in enumerate(rows):
				self.directoryTable.insertRow(row_number)
				for column_number, data in enumerate(row_data):
					item = QtWidgets.QTableWidgetItem()
					item.setData(QtCore.Qt.DisplayRole, data)
					self.directoryTable.setItem(self.directoryTable.rowCount() - 1, column_number, item)
			self.directoryTable.setSortingEnabled(True)

		if self.tableName == 'pays':
			try:
				self.directoryTable.disconnect()
			except Exception:
				pass
			self.directoryTable.doubleClicked['QModelIndex'].connect(self.editPay)
			self.newButton.pressed.connect(self.newPay)
			# self.searchColumn = 'name'
			self.setWindowTitle('Список входящих платежей')
			self.directoryTable.setColumnCount(5)
			self.directoryTable.setHorizontalHeaderLabels(['id', 'Дата', 'Партнёр', 'Проект', 'Сумма'])
			for index in range(self.directoryTable.columnCount()):
				self.directoryTable.setColumnWidth(index, self.settings.value('directoryTableColW_%s_%s' % (index, self.tableName), 50))
			self.directoryTable.hideColumn(0)
			if self.lineEdit.text() != '':
				whereTxt += " and name LIKE '%%%s%%' or project LIKE '%%%s%%'" % (self.lineEdit.text(), self.lineEdit.text())
			rows = query('''
				select
					pays_view.id, pays_view.dt, pays_view.name, pays_view.project, pays_view.amount
				from pays_view
				where %s  
				order by pay_dt
			''' % whereTxt)
			for row_number, row_data in enumerate(rows):
				self.directoryTable.insertRow(row_number)
				for column_number, data in enumerate(row_data):
					item = QtWidgets.QTableWidgetItem()
					if type(data) == decimal.Decimal:
						data = float(data)
					if type(data) in (datetime.datetime,):
						item = DateTimeWidgetItem(str(data.strftime("%d %b %y")), str(data))
						item.setTextAlignment((Qt.AlignCenter | Qt.AlignVCenter))
						self.directoryTable.setItem(self.directoryTable.rowCount() - 1, column_number, item)
						continue
					item.setData(QtCore.Qt.DisplayRole, data)
					self.directoryTable.setItem(self.directoryTable.rowCount() - 1, column_number, item)
			self.directoryTable.setSortingEnabled(True)

	def closeEvent(self, event):
		self.savepos()

	def moveEvent(self, e):
		self.savepos()

	def resizeEvent(self, e):
		self.savepos()

	def savepos(self):
		self.settings.setValue("directory_%s_window_size" % self.tableName, self.size())
		self.settings.setValue("directory_%s_window_pos" % self.tableName, self.pos())
		for index in range(self.directoryTable.columnCount()):
			self.settings.setValue("directoryTableColW_%s_%s" % (index, self.tableName), self.directoryTable.columnWidth(index))

	def eventFilter(self, obj, event):
		if obj == self.directoryTable:
	# 		# if event.type() == QEvent.MouseButtonRelease:
	# 		# 	self.savepos()
			if event.type() == QEvent.KeyPress:
				if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
					if self.tableName == 'partners': self.editPartner()
					if self.tableName == 'pays': self.editPay()
				if event.key() == QtCore.Qt.Key_F5:
					self.tableFill()
		return super(DirectoryWindow, self).eventFilter(obj, event)

	def editPartner(self):
		self.savepos()
		try:
			pID = int(self.directoryTable.item(self.directoryTable.currentItem().row(), 0).text())
		except:
			return
		partEdit = PartnerEdit(self)
		partEdit.partnerId = pID
		partEdit.mode = 'edit'
		partEdit.recordRead()
		currentRow = self.directoryTable.currentRow()
		if partEdit.exec():
			self.tableFill()
		self.directoryTable.selectRow(currentRow)

	def newPartner(self):
		self.savepos()
		partEdit = PartnerEdit(self)
		partEdit.mode = 'new'
		if partEdit.exec():
			currentRow = self.directoryTable.currentRow()
			self.tableFill()
			self.directoryTable.selectRow(currentRow)

	def editPay(self):
		self.savepos()
		try:
			pID = int(self.directoryTable.item(self.directoryTable.currentItem().row(), 0).text())
		except:
			return
		payEdit = PayEdit(self)
		payEdit.payId = pID
		payEdit.mode = 'edit'
		payEdit.recordRead()
		if payEdit.exec():
			currentRow = self.directoryTable.currentRow()
			self.tableFill()
			self.directoryTable.selectRow(currentRow)

	def newPay(self):
		payEdit = PayEdit(self)
		payEdit.mode = 'new'
		if payEdit.exec():
			currentRow = self.directoryTable.currentRow()
			self.tableFill()
			self.directoryTable.selectRow(currentRow)


class PartnerEdit(QtWidgets.QDialog, edit_partner.Ui_Dialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)

		self.partnerId = 0
		self.mode = 'edit'
		self.indexData = {}

		self.settings = QtCore.QSettings('AcademUpack', 'ERP')
		self.resize(self.settings.value("partner_edit_window_size", QtCore.QSize(300, 300)))
		self.move(self.settings.value("partner_edit_window_pos", QtCore.QPoint(100, 100)))
		self.buttonBox.accepted.connect(self.recordSave)
		self.packageEdit.installEventFilter(self)
		self.deliveryEdit.installEventFilter(self)

		self.contactsTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.contactsTable.customContextMenuRequested.connect(self.contactsMenu)

		self.contactsTable.horizontalHeader().setSectionHidden(0, True)
		self.contactsTable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
		self.contactsTable.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
		self.contactsTable.horizontalHeader().setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)
		self.contactsTable.horizontalHeader().setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)
		self.contactsTable.horizontalHeader().setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)

		fnt = QtGui.QFont()
		fnt.setPointSize(int(self.settings.value("font_size", 10)))
		self.setFont(fnt)
		self.contactsTable.setFont(fnt)

		rows = query('''
						select distinct
								name
							from
								partners
							where
								name != ''
		''')
		self.cNames = []
		for cN in rows:
			self.cNames.append(cN[0])
		completer = QtWidgets.QCompleter(self.cNames)
		completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
		self.nameEdit.setCompleter(completer)

		country = query('''
									select distinct
										country
									from
										partners
									where
										country != ''
										''')
		region = query('''
											select distinct
												region
											from
												partners
											where
												region != ''
												''')
		city = query('''
											select distinct
												city
											from
												partners
											where
												city != ''
												''')
		for c in country:
			co = c[0]
			self.countryComboBox.addItem(co)
		for r in region:
			ro = r[0]
			self.regionComboBox.addItem(ro)
		for ct in city:
			cto = ct[0]
			self.cityComboBox.addItem(cto)

	def recordRead(self):
		row = queryOne('''
						SELECT
							name,
							country,
							region,
							city,
							address,
							package,
							delivery,
							payment,
							payment_size,
							client,
							seller,
							own_firm,
							zip_code,
							post_address,
							creator_id,
							comments
						FROM 
							partners
						WHERE id = %s''' % self.partnerId)

		if row[0]: self.nameEdit.setText(row[0])
		if row[1]: self.countryComboBox.setCurrentText(row[1])
		if row[2]: self.regionComboBox.setCurrentText(row[2])
		if row[3]: self.cityComboBox.setCurrentText(row[3])
		if row[4]: self.addressEdit.setText(row[4])
		if row[5]: self.packageEdit.setText(row[5])
		if row[6]: self.deliveryEdit.setText(row[6])
		if row[7]:
			if row[7] == 'предоплата': self.prepayCheckBox.setChecked(True)
		if row[8]: self.paymentSizeSpinBox.setValue(int(row[8]))
		if row[9] == 1: self.clientCheckBox.setChecked(True)
		if row[10] == 1: self.sellerCheckBox.setChecked(True)
		if row[11] == 1: self.ownFirmCheckBox.setChecked(True)
		if row[12]: self.ZIPCodeEdit.setText(row[12])
		if row[13]: self.postAddressEdit.setText(row[13])
		if row[15]: self.commentsEdit.setText(row[15])

		rows = query('''
						select
							id,
							contact,
							post,
							tel,
							email,
							notification
						from
							partner_contacts
						where
							partner_id = %s
						order by id
		''' % self.partnerId)
		for row_number, row_data in enumerate(rows):
			self.contactsTable.insertRow(row_number)
			for column_number, data in enumerate(row_data):
				item = QtWidgets.QTableWidgetItem()
				itemChk = QtWidgets.QTableWidgetItem()
				item.setData(QtCore.Qt.DisplayRole, data)
				if column_number == 5:
					itemChk.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
					itemChk.setCheckState(QtCore.Qt.Unchecked)
					if data: itemChk.setCheckState(QtCore.Qt.Checked)
					self.contactsTable.setItem(self.contactsTable.rowCount() - 1, column_number, itemChk)
				else:
					self.contactsTable.setItem(self.contactsTable.rowCount() - 1, column_number, item)

		if self.mode == 'view':
			self.nameEdit.setReadOnly(True)
			self.countryComboBox.setEnabled(False)
			self.regionComboBox.setEnabled(False)
			self.cityComboBox.setEnabled(False)
			self.addressEdit.setReadOnly(True)
			self.ZIPCodeEdit.setReadOnly(True)
			self.postAddressEdit.setReadOnly(True)
			self.contactsTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
			self.prepayCheckBox.setEnabled(False)
			self.paymentSizeSpinBox.setReadOnly(True)
			self.clientCheckBox.setEnabled(False)
			self.sellerCheckBox.setEnabled(False)
			self.ownFirmCheckBox.setEnabled(False)
			self.commentsEdit.setReadOnly(True)
			self.packageEdit.setReadOnly(True)
			self.deliveryEdit.setReadOnly(True)
			self.buttonBox.setEnabled(False)

	def recordSave(self):
		if self.nameEdit.text() == '':
			msgBox = QtWidgets.QMessageBox()
			msgBox.setWindowTitle('Ошибка данных')
			msgBox.setText('Имя не должно быть пустым')
			msgBox.exec()
			return
		if self.mode == 'edit':
			queryInsert('''
							UPDATE partners
							SET
								name = %s,
								country = %s,
								region = %s,
								city = %s,
								address = %s,
								package = %s,
								delivery = %s,
								payment = %s,
								client = %s,
								seller = %s,
								zip_code = %s,
								post_address = %s,
								payment_size = %s,
								own_firm = %s,
								comments = %s
							WHERE id = %s
						''',
			            (self.nameEdit.text(),
			             self.countryComboBox.currentText(),
			             self.regionComboBox.currentText(),
			             self.cityComboBox.currentText(),
			             self.addressEdit.text(),
			             self.packageEdit.toPlainText(),
			             self.deliveryEdit.toPlainText(),
			             'предоплата' if self.prepayCheckBox.isChecked() else 'постоплата',
			             self.clientCheckBox.isChecked(),
			             self.sellerCheckBox.isChecked(),
			             self.ZIPCodeEdit.text(),
			             self.postAddressEdit.text(),
			             self.paymentSizeSpinBox.value(),
			             self.ownFirmCheckBox.isChecked(),
			             self.commentsEdit.toPlainText(),
			             self.partnerId
			             ))
		if self.mode == 'new':
			if self.nameEdit.text() in self.cNames:
				msgBox = QtWidgets.QMessageBox()
				msgBox.setWindowTitle('Ошибка данных')
				msgBox.setText('Такое имя уже существует. Имена должны быть уникальными.')
				msgBox.exec()
				return
			if self.nameEdit.text() == '':
				msgBox = QtWidgets.QMessageBox()
				msgBox.setWindowTitle('Ошибка данных')
				msgBox.setText('Имя не должно быть пустым')
				msgBox.exec()
				return
			self.partnerId = queryInsert('''
						INSERT INTO partners
						(
							name,
							country,
							region,
							city,
							address,
							package,
							delivery,
							payment,
							client,
							seller,
							zip_code,
							post_address,
							payment_size,
							own_firm,
							creator_id
						)
						values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
			            (
				            self.nameEdit.text(),
				            self.countryComboBox.currentText(),
				            self.regionComboBox.currentText(),
				            self.cityComboBox.currentText(),
				            self.addressEdit.text(),
				            self.packageEdit.toPlainText(),
				            self.deliveryEdit.toPlainText(),
				            'предоплата' if self.prepayCheckBox.isChecked() else 'постоплата',
				            self.clientCheckBox.isChecked(),
				            self.sellerCheckBox.isChecked(),
				            self.ZIPCodeEdit.text(),
				            self.postAddressEdit.text(),
				            self.paymentSizeSpinBox.value(),
				            self.ownFirmCheckBox.isChecked(),
				            loginInfo.get('id')
			            ))

		queryInsert('delete from partner_contacts where partner_id = %s', (self.partnerId,))
		for row_number in range(self.contactsTable.rowCount()):
			queryInsert('''
						insert into
							partner_contacts
						(
							partner_id,
							contact,
							post,
							tel,
							email,
							notification
						)
						values
						(%s,%s,%s,%s,%s,%s)
			''',(
				self.partnerId,
				'' if (self.contactsTable.item(row_number, 1) == None) or (self.contactsTable.item(row_number, 1).text() == '') else self.contactsTable.item(row_number, 1).text(),
				'' if (self.contactsTable.item(row_number, 2) == None) or (self.contactsTable.item(row_number, 2).text() == '') else self.contactsTable.item(row_number, 2).text(),
				'' if (self.contactsTable.item(row_number, 3) == None) or (self.contactsTable.item(row_number, 3).text() == '') else self.contactsTable.item(row_number, 3).text(),
				'' if (self.contactsTable.item(row_number, 4) == None) or (self.contactsTable.item(row_number, 4).text() == '') else self.contactsTable.item(row_number, 4).text(),
				True if self.contactsTable.item(row_number, 5).checkState() else False
			))


		self.accept()

	def moveEvent(self, e):
		self.savepos()

	def resizeEvent(self, e):
		self.savepos()

	def savepos(self):
		self.settings.setValue("partner_edit_window_size", self.size())
		self.settings.setValue("partner_edit_window_pos", self.pos())

	def eventFilter(self, obj, event):
		if (obj == self.packageEdit) or (obj == self.deliveryEdit):
			if (event.type() == QEvent.KeyPress) and (
					event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return) and (
					event.modifiers() == QtCore.Qt.ControlModifier)):
				self.recordSave()
				self.accept()
		return super(PartnerEdit, self).eventFilter(obj, event)

	def contactsMenu(self, pos):
		if self.mode == 'view': return
		selected = self.contactsTable.selectedIndexes()
		self.menu = QtWidgets.QMenu(self)
		if selected:
			deleteAction = self.menu.addAction('Удалить строку')
			deleteAction.triggered.connect(lambda: self.removeRows(selected, self.contactsTable))
		addAction = self.menu.addAction('Вставить строку')
		addAction.triggered.connect(lambda: self.addRow(self.contactsTable))
		self.menu.popup(QtGui.QCursor.pos())

	def removeRows(self, indexes, table):
		# get unique row numbers
		rows = set(index.row() for index in indexes)
		# remove rows in *REVERSE* order!
		for row in sorted(rows, reverse=True):
			table.removeRow(row)

	def addRow(self, table):
		table.insertRow(table.rowCount())
		item = QtWidgets.QTableWidgetItem()
		item.setText('')
		itemChk = QtWidgets.QTableWidgetItem()
		itemChk.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)
		itemChk.setCheckState(QtCore.Qt.Unchecked)
		for col in range(table.columnCount()-1):
			table.setItem(table.rowCount() - 1, col, item)
		table.setItem(table.rowCount() - 1, 5, itemChk)

class PayEdit(QtWidgets.QDialog, edit_pay.Ui_Dialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)

		self.payId = 0
		self.mode = 'edit'
		self.partnerIndexData = {}
		self.projectIndexData = {}

		self.settings = QtCore.QSettings('AcademUpack', 'ERP')
		self.resize(self.settings.value("pay_edit_window_size", QtCore.QSize(300, 300)))
		self.move(self.settings.value("pay_edit_window_pos", QtCore.QPoint(100, 100)))
		self.buttonBox.accepted.connect(self.recordSave)
		self.partnerComboBox.currentIndexChanged.connect(self.projectComboFill)
		self.projectComboBox.currentIndexChanged.connect(self.tableFill)
		self.dateEdit.setDate(QDate.currentDate())
		self.oldPaysTable.horizontalHeader().sectionResized.connect(self.savepos)

		fnt = QtGui.QFont()
		fnt.setPointSize(int(self.settings.value("font_size", 10)))
		self.setFont(fnt)

		self.partnerComboFill()
		self.projectComboFill()

	def recordRead(self):
		row = queryOne('''
						SELECT DISTINCT
							id,
							date_format(dt, '%%Y'),
							date_format(dt, '%%m'),
							date_format(dt, '%%d'),
							partner_id,
							project_id,
							amount,
							comment
						FROM 
							pays_view
						WHERE id = %s''' % self.payId)

		if row[1]: self.dateEdit.setDate(QDate(int(row[1]), int(row[2]), int(row[3])))
		if row[4]: self.partnerComboBox.setCurrentIndex(self.partnerComboBox.findData(row[4]))
		if row[5]: self.projectComboBox.setCurrentIndex(self.projectComboBox.findData(row[5]))
		if row[6]: self.amountSpinBox.setValue(row[6])
		if row[7]: self.commentEdit.setText(row[7])

	def recordSave(self):
		if self.projectComboBox.count() == 0:
			msgBox = QtWidgets.QMessageBox()
			msgBox.setWindowTitle('Ошибка данных')
			msgBox.setText('Для добавления платежа необходимо выбрать проект')
			msgBox.exec()
			return
		if self.mode == 'edit':
			queryInsert('''
							UPDATE pays
							SET
								project_id = %s,
								pay_dt = %s,
								creator_id = %s,
								amount = %s,
								comment = %s
							WHERE id = %s
						''',
			            (
				            self.projectComboBox.currentData(),
				            self.dateEdit.dateTime().toString('yyyy-MM-dd hh:mm:ss'),
				            loginInfo.get('id'),
				            self.amountSpinBox.value(),
				            self.commentEdit.toPlainText(),
				            self.payId
			            ))
		if self.mode == 'new':
			queryInsert('''
						INSERT INTO pays
						(
							project_id,
							pay_dt,
							creator_id,
							amount,
							comment
						)
						values (%s, %s, %s, %s, %s)''',
			            (
				            self.projectComboBox.currentData(),
				            self.dateEdit.dateTime().toString('yyyy-MM-dd hh:mm:ss'),
				            loginInfo.get('id'),
				            self.amountSpinBox.value(),
				            self.commentEdit.toPlainText()
			            ))
		self.accept()

	def tableFill(self):
		self.oldPaysTable.setSortingEnabled(False)
		while self.oldPaysTable.rowCount() > 0:
			self.oldPaysTable.removeRow(0)
		whereTxt = '1'

		try:
			self.oldPaysTable.disconnect()
		except Exception:
			pass
		self.oldPaysTable.setColumnCount(3)
		self.oldPaysTable.setHorizontalHeaderLabels(['id', 'Дата', 'Сумма'])
		if self.settings.value("old_pay_table_state"):
			self.oldPaysTable.horizontalHeader().restoreState(self.settings.value("old_pay_table_state"))
		self.oldPaysTable.hideColumn(0)
		if (self.projectComboBox.currentData() != '0') and (self.projectComboBox.currentData() != None):
			rows = query('''
				select
					pays_view.id, pays_view.dt, pays_view.amount
				from pays_view
				where project_id=%s  
				order by pay_dt
			''' % self.projectComboBox.currentData())
		else:
			rows = ()
		for row_number, row_data in enumerate(rows):
			self.oldPaysTable.insertRow(row_number)
			for column_number, data in enumerate(row_data):
				item = QtWidgets.QTableWidgetItem()
				if type(data) == decimal.Decimal:
					data = float(data)
				if type(data) in (datetime.datetime,):
					item = DateTimeWidgetItem(str(data.strftime("%d %b %y")), str(data))
					item.setTextAlignment((Qt.AlignCenter | Qt.AlignVCenter))
					self.oldPaysTable.setItem(self.oldPaysTable.rowCount() - 1, column_number, item)
					continue
				item.setData(QtCore.Qt.DisplayRole, data)
				self.oldPaysTable.setItem(self.oldPaysTable.rowCount() - 1, column_number, item)
		self.oldPaysTable.setSortingEnabled(True)

	def closeEvent(self, e):
		self.savepos()

	def resizeEvent(self, e):
		self.savepos()

	def savepos(self):
		self.settings.setValue("pay_edit_window_size", self.size())
		self.settings.setValue("pay_edit_window_pos", self.pos())
		self.settings.setValue("old_pay_table_state", self.oldPaysTable.horizontalHeader().saveState())

	def eventFilter(self, obj, event):
		if obj == self.commentEdit:
			if (event.type() == QEvent.KeyPress) and (
					event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return) and (
					event.modifiers() == QtCore.Qt.ControlModifier)):
				self.recordSave()
				self.accept()
		return super(PayEdit, self).eventFilter(obj, event)

	def partnerComboFill(self):
		self.partnerComboBox.clear()
		self.partnerComboBox.addItem('', '0')
		for row in query('''SELECT DISTINCT
								`partners`.`name` AS `name`,
								`projects`.`partner_id` AS `partner_id`,
								`partners`.`id` AS `id`
							FROM `partners`
							LEFT JOIN `projects` ON `partners`.`id` = `projects`.`partner_id`
							WHERE `partner_id`
							ORDER BY `partners`.`name`'''):
			self.partnerComboBox.addItem(row[0], str(row[1]))

	def projectComboFill(self):
		self.projectComboBox.clear()
		self.projectComboBox.addItem('', '0')
		if self.partnerComboBox.currentData() == '0':
			self.projectComboBox.setEnabled(False)
		else:
			self.projectComboBox.setEnabled(True)
			for row in query('''select `id`, `create_dt`, `partner_name`, `partner_id`, `project_name`, `invoice_num`, `status_id`
									from `projects_view`
									where `partner_id`=%s
									order by `create_dt` desc''' % self.partnerComboBox.currentData()):
				if row[5]: invoice = '  |  счёт ' + row[5]
				else: invoice = ''
				self.projectComboBox.addItem(row[1].strftime("%d %b %y") + '  |  ' + row[4] + invoice, row[0])


class ProjectEdit(QtWidgets.QDialog, edit_project.Ui_Dialog):
	signalAccept = QtCore.pyqtSignal(bool)
	
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setupUi(self)
		
		self.setWindowFlag(QtCore.Qt.WindowCloseButtonHint, False)
		self.isFormEdited = False

		self.projectId = 0
		self.mode = 'edit'
		self.indexData = {}
		self.createDateTime = QDateTime.currentDateTime()
		self.recordBlocked = False

		self.commentBrowser.anchorClicked.connect(QtGui.QDesktopServices.openUrl)
		self.commentBrowser.clear()
		self.commentBrowser.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.commentBrowser.customContextMenuRequested.connect(self.commentBrowserMenu)

		self.splitter.splitterMoved.connect(self.savepos)

		self.settings = QtCore.QSettings('AcademUpack', 'ERP')
		if self.settings.value("project_edit_window_geometry"):
			self.restoreGeometry(self.settings.value("project_edit_window_geometry"))
		if self.settings.value("project_edit_window_splitter"):
			self.splitter.restoreState(self.settings.value("project_edit_window_splitter"))

		# Set font parameters
		fnt = QtGui.QFont()
		fnt.setPointSize(int(self.settings.value("font_size", 12)))
		self.setFont(fnt)
		self.folderEdit.setFont(fnt)

		self.partnerComboBox.completer.popup().setFont(self.font())

		# self.buttonBox.accepted.connect(self.signalAcceptEmit)
		self.accepted.connect(self.signalAcceptEmit)
		self.rejected.connect(self.signalRejectEmit)
		
		# set edited flag
		self.commentsEdit.textChanged.connect(self.setFormEdited)
		self.partnerComboBox.currentIndexChanged.connect(self.setFormEdited)
		self.deadlineEdit.dateChanged.connect(self.setFormEdited)
		self.statusComboBox.currentIndexChanged.connect(self.setFormEdited)
		self.projectNameEdit.textChanged.connect(self.setFormEdited)
		self.quantitySpinBox.valueChanged.connect(self.setFormEdited)
		self.priceSpinBox.valueChanged.connect(self.setFormEdited)
		self.amountSpinBox.valueChanged.connect(self.setFormEdited)
		self.folderEdit.textChanged.connect(self.setFormEdited)
		self.invoiceNeedCheckBox.stateChanged.connect(self.setFormEdited)
		self.invoiceNumberEdit.textChanged.connect(self.setFormEdited)
		self.invoiceDateEdit.dateChanged.connect(self.setFormEdited)
		
		
		self.spinsConnect()
		self.newPartnerButton.pressed.connect(self.newPartner)
		self.infoPartnerButton.pressed.connect(self.infoPartner)
		self.addPayButton.pressed.connect(self.addPay)
		self.invoiceNumberEdit.textChanged.connect(self.invoiceNeedUncheck)
		self.invoiceDateEdit.setDate(self.createDateTime.date())
		self.deadlineEdit.setDate(self.createDateTime.date().addDays(-1))
		self.deadlineEdit.setSpecialValueText('---')
		self.deadlineEdit.setMinimumDate(self.createDateTime.date().addDays(-1))
		self.deadlineEdit.setMinimumDateTime(self.createDateTime.addDays(-1))
		self.statusComboBox.addItem('', '0')
		self.partnerComboBox.addItem('', '0')
		self.partnerComboBox.currentIndexChanged.connect(self.projectNameCompleter)
		self.commentsEdit.installEventFilter(self)
		self.commentBrowserTemplate = '''<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN">
<html><head><meta name="qrichtext" content="1" />
</head>
<body style=" font-family:'MS Shell Dlg 2'; font-weight:400; font-style:normal;">$template_new$<p align="left">$template_old$</p>
</body></html>'''

		self.timer = QtCore.QTimer(self)
		self.timer.timeout.connect(self.blockerUpdate)
		self.timer.setInterval(5000)
	
	def setFormEdited(self):
		self.isFormEdited = True
		print(self.isFormEdited)

	def commentBrowserMenu(self):
		try:
			lastCommentUserID = queryOne('select user_id from project_comments where project_id=%s order by id desc limit 1' % self.projectId)[0]
		except:
			return
		if lastCommentUserID == loginInfo.get('id'):
			self.commentsMenu = QtWidgets.QMenu(self)
			commentEditAction = self.commentsMenu.addAction('Редактировать последний комментарий')
			commentEditAction.triggered.connect(lambda: self.commentEdit('edit'))
			commentDeleteAction = self.commentsMenu.addAction('Удалить последний комментарий')
			commentDeleteAction.triggered.connect(lambda: self.commentEdit('delete'))
			if self.recordBlocked:
				commentEditAction.setEnabled(False)
				commentDeleteAction.setEnabled(False)
			self.commentsMenu.setFont(self.font())
			self.commentsMenu.popup(QtGui.QCursor.pos())

	def commentEdit(self, action: str):
		if action == 'edit':
			self.commentsEdit.setText(queryOne('select comment_body from project_comments where project_id=%s order by id desc limit 1' %
				                                   self.projectId)[0])
			queryOne('DELETE FROM project_comments WHERE project_id=%s ORDER BY id desc LIMIT 1;' % self.projectId)
			self.recordRead(notblock=True)
		self.isFormEdited = True
			
		if action == 'delete':
			queryOne('DELETE FROM project_comments WHERE project_id=%s ORDER BY id desc LIMIT 1;' % self.projectId)
			self.recordRead(notblock = True)
		# match action:
			# case 'edit':
				# self.commentsEdit.setText(queryOne('select comment_body from project_comments where project_id=%s order by id desc limit 1' %
				                                   # self.projectId)[0])
				# queryOne('DELETE FROM project_comments WHERE project_id=%s ORDER BY id desc LIMIT 1;' % self.projectId)
				# self.recordRead(notblock = True)
			# case 'delete':
				# queryOne('DELETE FROM project_comments WHERE project_id=%s ORDER BY id desc LIMIT 1;' % self.projectId)
				# self.recordRead(notblock = True)

	def signalAcceptEmit(self):
		self.recordSave()
		self.signalAccept.emit(True)
		self.blockerUpdate('clear')

	def signalRejectEmit(self):

		if (self.isFormEdited):
			reply = QtWidgets.QMessageBox.question(self, 'Закрыти окна', 'Данные изменены. Сохранить изменения?',
								   QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
	
			if reply == QtWidgets.QMessageBox.Yes:
				self.recordSave()
			else:
				print('Window closed, not save')

		self.signalAccept.emit(False)
		self.blockerUpdate('clear')

	def projectNameCompleter(self):
		if self.partnerComboBox.currentIndex() != 0:
			rows = queryDB('select project_name from projects_view where partner_id=%s', (self.partnerComboBox.currentData(),))
			pNames = []

			if rows:
				for pN in rows:
					pNames.append(pN[0])

			completer = QtWidgets.QCompleter(pNames)
			completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
			completer.setFilterMode(Qt.MatchContains)
			completer.popup().setFont(self.font())
			self.projectNameEdit.setCompleter(completer)

	def spinsConnect(self):
		self.quantitySpinBox.editingFinished.connect(self.quantityValidate)
		self.priceSpinBox.editingFinished.connect(self.priceValidate)
		self.amountSpinBox.editingFinished.connect(self.amountValidate)

	def msgDigitError(self, obj):
		msgBox = QtWidgets.QMessageBox()
		msgBox.setWindowTitle('Ошибка формата ввода')
		msgBox.setText('Нужно ввести число')
		msgBox.exec()
		obj.undo()
		obj.setFocus()
		obj.selectAll()

	def eventFilter(self, obj, event):
		if (event.type() == QEvent.KeyPress) and (obj == self.commentsEdit) and (
				event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return) and (
				event.modifiers() == QtCore.Qt.ControlModifier)):
			self.accept()
		
		return super(ProjectEdit, self).eventFilter(obj, event)
		

	def recordSave(self):
		self.blockerUpdate(mode='clear')
		if self.mode == 'edit':
			queryInsert('''
							UPDATE projects
							SET
								partner_id = %s,
								project_name = %s,
								quantity = %s,
								price = %s,
								amount = %s,
								folder = %s,
								deadline = %s,
								invoice_num = %s,
								invoice_date = %s,
								status_id = %s,
								changer_id = %s,
								invoice_need = %s
							WHERE id = %s;
						''',
			            (
			             self.partnerComboBox.currentData(),
			             self.projectNameEdit.text(),
			             self.quantitySpinBox.value(),
			             self.priceSpinBox.value(),
			             self.amountSpinBox.value(),
			             self.folderEdit.text(),
			             self.deadlineEdit.dateTime().toString('yyyy-MM-dd hh:mm:ss') if self.deadlineEdit.date() > self.createDateTime.date()\
							else '1900-01-01 01:01:01',
			             self.invoiceNumberEdit.text(),
			             self.invoiceDateEdit.dateTime().toString('yyyy-MM-dd hh:mm:ss'),
			             self.statusComboBox.currentData(),
			             loginInfo.get('id'),
			             int(self.invoiceNeedCheckBox.isChecked()),
			             self.projectId))
			if self.commentsEdit.toPlainText() != '':
				queryInsert('''							
								INSERT INTO project_comments
								(project_id,
								user_id,
								comment_body)
								values (%s, %s, %s)''', (self.projectId, loginInfo.get('id'), self.commentsEdit.toPlainText()))
		if self.mode == 'new':
			pNum = query('select max(num)+1 from projects')[0][0]
			queryInsert('''
						INSERT INTO projects
						(   num,
							create_dt,
							creator_id,
							partner_id,
							project_name,
							quantity,
							price,
							amount,
							folder,
							deadline,
							invoice_num,
							invoice_date,
							status_id,
							invoice_need
						)
						values (%s,current_timestamp(),%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
			            (pNum if pNum != None else 1,
			             loginInfo.get('id'),
			             self.partnerComboBox.currentData(),
			             self.projectNameEdit.text(),
			             self.quantitySpinBox.value(),
			             self.priceSpinBox.value(),
			             self.amountSpinBox.value(),
			             self.folderEdit.text(),
			             self.deadlineEdit.dateTime().toString('yyyy-MM-dd hh:mm:ss') if self.deadlineEdit.date() > self.createDateTime.date() \
				             else '1900-01-01 01:01:01',
			             self.invoiceNumberEdit.text(),
			             self.invoiceDateEdit.dateTime().toString('yyyy-MM-dd hh:mm:ss'),
			             self.statusComboBox.currentData(),
			             int(self.invoiceNeedCheckBox.isChecked())))
			if self.commentsEdit.toPlainText() != '':
				queryInsert('''							
								INSERT INTO project_comments
								(project_id,
								user_id,
								comment_body)
								values (%s, %s, %s)''',
				            (queryOne('select max(id) from projects')[0],
				             loginInfo.get('id'),
				             self.commentsEdit.toPlainText()))

	def recordRead(self, notblock = False):
		row = queryOne('''SELECT
								date_format(create_dt, '%%Y'),
								date_format(create_dt, '%%m'),
								date_format(create_dt, '%%d'),
								partner_id,
								quantity,
								amount,
								folder,
								date_format(deadline, '%%Y'),
								date_format(deadline, '%%m'),
								date_format(deadline, '%%d'),
								invoice_num,
								date_format(invoice_date, '%%Y'),
								date_format(invoice_date, '%%m'),
								date_format(invoice_date, '%%d'),
								comments,
								status_id,
								project_name,
								price,
								invoice_need
						FROM projects
						WHERE id = %s
						''' % self.projectId)
		comment_rows = query('''SELECT
										users.firstname,
										users.lastname,
										date_format(project_comments.comment_time, "%%d.%%m.%%Y %%H:%%i"),
										project_comments.comment_body,
										project_comments.user_id
									FROM
										project_comments
									LEFT JOIN users ON project_comments.user_id = users.id
									WHERE project_comments.project_id = %s
									ORDER by project_comments.comment_time DESC
								''' % self.projectId)

		block_row = queryOne('SELECT TIMESTAMPDIFF (SECOND, (SELECT block_dt FROM projects WHERE id=%s), CURRENT_TIMESTAMP())' % self.projectId)
		if (block_row[0] != None) and (block_row[0] < 10) and not notblock:
			block_row = queryOne('select blocker_id from projects where id=%s' % self.projectId)
			blocker = queryOne('select firstname, lastname from users where id=%s' % block_row[0])
			self.setWindowTitle(self.windowTitle() + ' *только для чтения* - редактирует %s %s' % (blocker[0], blocker[1]))
			self.buttonBox.setEnabled(False)
			self.statusComboBox.setEnabled(False)
			self.deadlineEdit.setReadOnly(True)
			self.partnerComboBox.setEnabled(False)
			self.projectNameEdit.setReadOnly(True)
			self.quantitySpinBox.setReadOnly(True)
			self.priceSpinBox.setReadOnly(True)
			self.amountSpinBox.setReadOnly(True)
			self.folderEdit.setReadOnly(True)
			self.invoiceNumberEdit.setReadOnly(True)
			self.invoiceDateEdit.setReadOnly(True)
			self.commentsEdit.setReadOnly(True)
			self.recordBlocked = True
		else:
			self.blockerUpdate(mode='update')
			self.recordBlocked = False

		self.createDateTime.setDate(QDate(int(row[0]), int(row[1]), int(row[2])))
		self.deadlineEdit.setMinimumDate(self.createDateTime.date().addDays(-1))
		self.deadlineEdit.setMinimumDateTime(self.createDateTime.addDays(-1))
		self.quantitySpinBox.setValue(row[4])
		self.amountSpinBox.setValue(row[5])
		self.priceSpinBox.setValue(row[17])
		if row[6]:  self.folderEdit.setText(str(row[6]))
		if row[10]: self.invoiceNumberEdit.setText(str(row[10]))
		if row[16]: self.projectNameEdit.setText(row[16])
		tmp = ''
		if (row[14] != '') and (row[14] != None):
			tmp = self.commentBrowserTemplate.replace('$template_old$', row[14].replace('\n', '<br>'))
			tmp = tmp.replace('$template_new$', self.commentEncoder(comment_rows))
			self.commentBrowser.setHtml(tmp)
		else:
			tmp = self.commentBrowserTemplate.replace('$template_old$', '')
			tmp = tmp.replace('$template_new$', self.commentEncoder(comment_rows))
			self.commentBrowser.setHtml(tmp)
		if row[7]:  self.deadlineEdit.setDate(QDate(int(row[7]), int(row[8]), int(row[9])))
		if row[11]: self.invoiceDateEdit.setDate(QDate(int(row[11]), int(row[12]), int(row[13])))
		self.partnerComboFill()
		if row[3]: self.partnerComboBox.setCurrentIndex(self.indexData.get(str(row[3])))
		self.statusComboFill()
		if row[15]: self.statusComboBox.setCurrentIndex(self.indexData.get(str(row[15])))
		self.invoiceNeedCheckBox.setChecked(True) if row[18] == 1 else self.invoiceNeedCheckBox.setChecked(False)
		
		self.isFormEdited = False

	def commentEncoder(self, comments = ()):
		template = '''<p align="center" style="font-weight: bold; margin-top:0px;margin-bottom:0px; margin-left:0px; margin-right:0px;-qt-block-indent:0; 
		text-indent:0px; 
		background-color:#e0e0e0;">
<span style=" background-color:#e0e0e0;">$mark$</span></p>
<p style=" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px;-qt-block-indent:0; text-indent:0px; background-color:#ffffff;">
<span style=" background-color:#ffffff;">$comment$</span></p>'''
		result = ''
		if comments != None:
			for com in comments:
				restemp = template.replace('$mark$', str(com[2]) + ' ' + str(com[0]) + ' ' + str(com[1]))
				comment = ''
				for s in str(com[3]).split('\n'):
					if s.startswith('file:') or s.startswith('http:') or s.startswith('https:') or s.startswith('ftp:'):
						comment = comment + '<a href="' + s.replace(' ', '%20') + '">' + s + '</a><br>'
					else:
						comment = comment + s + '<br>'
				restemp = restemp.replace('$comment$', comment)
				result = result + restemp
		return result

	def blockerUpdate(self, mode='update'):
		if mode == 'update':
			if not self.timer.isActive():
				self.timer.start()
			queryInsert('''UPDATE
										projects
									SET
										block_dt=current_timestamp(),
										blocker_id=%s
									WHERE
										id=%s''',
			            (loginInfo.get('id'),
			             self.projectId))
		if mode == 'clear':
			self.timer.stop()
			queryInsert('''UPDATE
										projects
									SET
										block_dt=current_timestamp(),
										blocker_id=0
									WHERE
										id=%s''',
			            (loginInfo.get('id'),
			             ))

	def quantityValidate(self):
		self.amountSpinBox.setValue(self.priceSpinBox.value() * self.quantitySpinBox.value())

	def priceValidate(self):
		self.amountSpinBox.setValue(self.priceSpinBox.value() * self.quantitySpinBox.value())

	def amountValidate(self):
		if self.quantitySpinBox:
			self.priceSpinBox.setValue(self.amountSpinBox.value() / self.quantitySpinBox.value())
		else:
			self.priceSpinBox.setValue(0)

	def statusComboFill(self):
		self.statusComboBox.clear()
		self.indexData['0'] = 0
		index = 0
		for row in query('select `name`, `id`, `order` from `project_statuses` order by `order`'):
			self.statusComboBox.addItem(row[0], str(row[1]))
			self.indexData[str(row[1])] = index
			index += 1

	def partnerComboFill(self):
		self.partnerComboBox.clear()
		self.partnerComboBox.addItem('', '0')
		self.indexData['0'] = 0
		index = 1
		for row in query('select `name`, `id` from `partners` order by `name`'):
			self.partnerComboBox.addItem(row[0], str(row[1]))
			self.indexData[str(row[1])] = index
			index += 1

	def newPartner(self):
		partNew = PartnerEdit()
		partNew.mode = 'new'
		partNew.exec_()
		prt = self.partnerComboBox.currentIndex()
		self.partnerComboFill()
		self.partnerComboBox.setCurrentIndex(prt)

	def infoPartner(self):
		if self.partnerComboBox.currentData() != '0':
			partInfo = PartnerEdit(self)
			partInfo.mode = 'view'
			partInfo.partnerId = int(self.partnerComboBox.currentData())
			partInfo.recordRead()
			partInfo.buttonBox.setEnabled(False)
			partInfo.exec_()

	def addPay(self):
		if self.mode == 'edit':
			payEdit = PayEdit(self)
			payEdit.partnerComboBox.setCurrentIndex(payEdit.partnerComboBox.findData(self.partnerComboBox.currentData()))
			payEdit.projectComboBox.setCurrentIndex(payEdit.projectComboBox.findData(self.projectId))
			payEdit.mode = 'new'
			payEdit.exec()

	def closeEvent(self, e):
		self.savepos()
		self.blockerUpdate(mode='clear')

	def moveEvent(self, e):
		self.savepos()

	def resizeEvent(self, e):
		self.savepos()

	def savepos(self):
		self.settings.setValue("project_edit_window_geometry", self.saveGeometry())
		self.settings.setValue("project_edit_window_splitter", self.splitter.saveState())

	def invoiceNeedUncheck(self):
		self.invoiceNeedCheckBox.setChecked(False)

class PaddingDelegate(QtWidgets.QStyledItemDelegate):
	def __init__(self, padding=1, parent=None):
		super(PaddingDelegate, self).__init__(parent)
		self._padding = '   ' * max(1, padding)

	def displayText(self, text, locale):
		return self._padding + str(text)

	def createEditor(self, parent, option, index):
		editor = super().createEditor(parent, option, index)
		margins = editor.textMargins()
		padding = editor.fontMetrics().width(self._padding) + 1
		margins.setLeft(margins.left() + padding)
		editor.setTextMargins(margins)
		return editor

class App(QtWidgets.QMainWindow, main_form_concept.Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)

		self.autoFilter = True

		# from PyQt5.QtGui import QPalette
		# pal = self.projectTable.palette()
		# pal.setColor(QPalette.Inactive, QPalette.Highlight, pal.color(QPalette.Active, QPalette.Highlight))
		# self.projectTable.setPalette(pal)

		self.projectTable.installEventFilter(self)
		self.mainDock.installEventFilter(self)
		self.partnerEdit.installEventFilter(self)
		self.projectNameEdit.installEventFilter(self)
		self.filterList.installEventFilter(self)

		self.projectTable.doubleClicked['QModelIndex'].connect(self.editProject)
		self.projectTable.horizontalHeader().sectionResized.connect(self.projectTable.resizeRowsToContents)
		self.projectTable.horizontalHeader().setSectionsMovable(True)
		self.settings = QtCore.QSettings('AcademUpack', 'ERP')
		if self.settings.value("main_window_state"):
			self.restoreState(self.settings.value("main_window_state"))
		if self.settings.value("main_window_geometry"):
			self.restoreGeometry(self.settings.value("main_window_geometry"))
		try:
			self.projectTable.horizontalHeader().setSortIndicator(self.settings.value('projectTableSortSection'), self.settings.value('projectTableSortOrder'))
		except:
			pass

		fnt = QtGui.QFont()
		fnt.setPointSize(int(self.settings.value("font_size", 10)))
		self.setFont(fnt)
		self.mainDock.setFont(fnt)

		self.lists_clients.triggered.connect(self.listOfPartners)
		self.pays.triggered.connect(self.listOfPays)
		self.settings_interface.triggered.connect(self.settingsInterface)
		self.filterButton.pressed.connect(self.tableFill)
		self.filterClearButton.pressed.connect(self.filterClear)
		self.newButton.pressed.connect(self.newProject)
		self.filterButton.setIcon(QtGui.QIcon(':/icons/sync'))
		self.filterClearButton.setIcon(QtGui.QIcon(':/icons/filter'))
		self.newButton.setIcon(QtGui.QIcon(':/icons/description'))

		# сработка фильтров
		self.filterList.itemChanged.connect(self.tableFill)

		self.projectTable.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.projectTable.customContextMenuRequested.connect(self.projectTableMenu)

		# наполнение дополнения поля поиска партнёра
		self.partner_autocomplete_model = QtGui.QStandardItemModel()
		rows = query('select distinct partner_name from projects_view')
		if rows:
			for row in rows:
				self.partner_autocomplete_model.appendRow(QtGui.QStandardItem(row[0]))
		self.partner_completer = QtWidgets.QCompleter()
		self.partner_completer.setModel(self.partner_autocomplete_model)
		self.partnerEdit.setCompleter(self.partner_completer)
		self.partner_completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
		self.partner_completer.setFilterMode(Qt.MatchContains)
		self.partner_completer.setMaxVisibleItems(30)
		self.partner_completer.popup().setFont(self.font())

		# наполнение дополнения поля поиска проекта
		self.project_autocomplete_model = QtGui.QStandardItemModel()
		rows = query('select distinct project_name from projects_view')
		if rows:
			for row in rows:
				self.project_autocomplete_model.appendRow(QtGui.QStandardItem(row[0]))
		self.project_completer = QtWidgets.QCompleter()
		self.project_completer.setModel(self.project_autocomplete_model)
		self.projectNameEdit.setCompleter(self.project_completer)
		self.project_completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
		self.project_completer.setFilterMode(Qt.MatchContains)
		self.project_completer.setMaxVisibleItems(30)
		self.project_completer.popup().setFont(self.font())

		# триггеры фильтров
		self.partnerEdit.editingFinished.connect(self.tableFill)
		self.projectNameEdit.editingFinished.connect(self.tableFill)
		# self.statusComboBox.currentIndexChanged.connect(self.tableFill)
		# self.releasedCheckBox.stateChanged.connect(self.tableFill)
		# self.invoiceNeedCheckBox.stateChanged.connect(self.tableFill)

		# self.delegate = PaddingDelegate()
		# self.projectTable.setItemDelegate(self.delegate)
		self.projectTable.setColumnCount(11)
		self.projectTable.setHorizontalHeaderLabels(
			['id', 'Номер', 'Дата', 'Партнёр', 'Наименование', 'Кол-во', 'Сумма', 'Срок', 'Готов', 'Счёт/Оплата', 'Статус'])
		self.projectTable.hideColumn(0)

		if self.settings.value("project_table_state"):
			self.projectTable.horizontalHeader().restoreState(self.settings.value("project_table_state"))
		fsize = self.settings.value("font_size", 10)
		self.projectTable.setStyleSheet('QHeaderView::section{alternate-background-color: #FFFFFF; font-size: %spt;}' % fsize)
		self.menu.setStyleSheet('font: %spt' % fsize)
		self.menu_2.setStyleSheet('font: %spt' % fsize)
		self.menu_3.setStyleSheet('font: %spt' % fsize)

		user_settings_query = query("SELECT  `id`,`login`, `firstname`, `middlename`, `lastname`, `is_dictionary`,\
		`is_users`,  `is_projects`\
		FROM `users`\
		WHERE `login` = '%s'" % loginInfo.get('user'))
		user_settings = user_settings_query[0]
		loginInfo['id'] = user_settings[0]
		user_firstname = user_settings[2]
		user_middlename = user_settings[3]
		user_lastname = user_settings[4]
		user_is_dictionary = user_settings[5]
		user_is_users = user_settings[6]
		user_is_projects = user_settings[7]

		# устанавливаем начальные значения фильтра

		# self.datesInit()  # даты

		self.statusFill()  # статусы
		# self.statusComboBox.setCurrentIndex(0)

		# наполняем таблицу
		self.tableFill()

	def partnerCompleter(self):
		self.partner_autocomplete_model.clear()
		rows = query('select distinct partner_name from projects_view')

		if rows:
			for row in rows:
				self.partner_autocomplete_model.appendRow(QtGui.QStandardItem(row[0]))

	def projectCompleter(self):
		self.project_autocomplete_model.clear()
		rows = query("select distinct project_name from projects_view where partner_name like '%%%s%%'" % self.partnerEdit.text())

		if rows:
			for row in rows:
				self.project_autocomplete_model.appendRow(QtGui.QStandardItem(row[0]))

	# обработка событий
	def eventFilter(self, obj, event):
		# if (event.type() == QEvent.KeyPress) or (event.type() == QEvent.MouseButtonPress):
		# 	if (obj == self.statusComboBox):
		# 		self.statusFill()
		if (event.type() == QEvent.KeyPress) and (obj == self.projectTable):
			if event.key() in (QtCore.Qt.Key_Enter, QtCore.Qt.Key_Return):
				self.editProject()
		if (event.type() == QEvent.KeyPress) and (event.key() == QtCore.Qt.Key_F5) \
				and ((obj == self.projectTable)
				or (obj == self.mainDock)):
			self.tableFill()
		return super(App, self).eventFilter(obj, event)

	def statusFill(self):
		# curIndex = self.statusComboBox.currentIndex()
		# self.statusComboBox.clear()
		# self.statusComboBox.addItem('', '0')
		# for row in query('select `name`, `id` from `project_statuses` order by `id`'):
		# 	self.statusComboBox.addItem(row[0], str(row[1]))
		# self.statusComboBox.setCurrentIndex(curIndex)
		pass

	def settingsInterface(self):
		sI = InterfaceSettings(self)
		sI.signalSpinChange.connect(self.fontSizeChange)
		sI.show()

	def fontSizeChange(self, size):
		fnt = QtGui.QFont()
		fnt.setPointSize(size)
		self.setFont(fnt)
		self.projectTable.setStyleSheet('QHeaderView::section{font-size:%spt;}' % size)
		self.menu.setStyleSheet('font: %spt' % size)
		self.menu_2.setStyleSheet('font: %spt' % size)
		self.menu_3.setStyleSheet('font: %spt' % size)
		self.tableFill()

	def listOfPartners(self):
		listPart = DirectoryWindow(self)
		listPart.tableName = 'partners'
		listPart.tableFill()
		listPart.exec()

	def listOfPays(self):
		listPays = DirectoryWindow(self)
		listPays.tableName = 'pays'
		listPays.tableFill()
		listPays.exec()

	def editProject(self):
		try:
			pID = int(self.projectTable.item(self.projectTable.currentItem().row(), 0).text())
		except:
			return
		pEdit = ProjectEdit(self)
		pEdit.projectId = pID
		pEdit.mode = 'edit'
		pEdit.recordRead()
		pEdit.signalAccept.connect(self.editProjectAccept)
		pEdit.show()
		# if pEdit.show():
		# 	currentRow = self.projectTable.currentRow()
		# 	self.tableFill()
		# 	self.projectTable.selectRow(currentRow)
		# pEdit.blockerUpdate(mode='clear')

	def editProjectAccept(self, accept):
		if accept:
			currentRow = self.projectTable.currentRow()
			self.tableFill()
			self.projectTable.selectRow(currentRow)

	def closeEvent(self, e):  # сохранение позиции окна и главной таблицы
		self.settings.setValue("project_table_state", self.projectTable.horizontalHeader().saveState())
		self.settings.setValue("main_window_state", self.saveState())
		self.settings.setValue("main_window_geometry", self.saveGeometry())

	def tableFill(self):  # наполнение таблицы
		self.projectTable.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.WaitCursor))
		if self.autoFilter:
			self.projectTable.setSortingEnabled(False)
			while self.projectTable.rowCount() > 0:
				self.projectTable.removeRow(0)
			whereTxt = ''
			for i in range(0, 10):
				if self.filterList.item(i).checkState() == QtCore.Qt.Checked:
					if whereTxt != '': whereTxt += ' or'
					whereTxt += f' status_name LIKE "{self.filterList.item(i).text()}"'
			if whereTxt != '':
				whereTxt = 'where (' + whereTxt + ')'
			else:
				whereTxt = 'where 1' + whereTxt
			if self.filterList.item(10).checkState() == QtCore.Qt.Checked:
				if whereTxt != '':
					whereTxt += ' and'
				whereTxt += ' invoice_need = 1'
			if self.partnerEdit.text() != '':
				if whereTxt != '': whereTxt += ' and'
				whereTxt += " partner_name LIKE '%%%s%%'" % self.partnerEdit.text()
			if self.projectNameEdit.text() != '':
				if whereTxt != '': whereTxt += ' and'
				whereTxt += " project_name LIKE '%%%s%%'" % self.projectNameEdit.text()
			rows = query('''SELECT
								id,
								num,
								create_dt,
								partner_name,
								project_name,
								quantity,
								amount,
								deadline,
								done_dt,
								invoice_num,
								status_name,
								invoice_need
							FROM
								projects_view
							%s''' % whereTxt)
			for row_number, row_data in enumerate(rows):
				invoice_need = row_data[11]
				self.projectTable.insertRow(row_number)
				for column_number, data in enumerate(row_data):
					item = QtWidgets.QTableWidgetItem()
					item.setFont(self.font())
					if type(data) in (decimal.Decimal, int, float): item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
					if type(data) in (datetime.datetime, ):
						if data.strftime("%Y") == '1900':
							item = DateTimeWidgetItem('', str(data))
						else:
							item = DateTimeWidgetItem(str(data.strftime("%d %b %y")), str(data))
						item.setTextAlignment((Qt.AlignCenter | Qt.AlignVCenter))
						item.setFont(self.font())
						self.projectTable.setItem(self.projectTable.rowCount() - 1, column_number, item)
						continue
					if type(data) == decimal.Decimal: data = float(data)

					item.setData(QtCore.Qt.DisplayRole, data)
					if str(data) == 'техкарта': item.setBackground(QtGui.QBrush(QtGui.QColor('#d9d9d9')))
					if str(data) == 'в работу': item.setBackground(QtGui.QBrush(QtGui.QColor('#f4cccc')))
					if str(data) == 'в процессе': item.setBackground(QtGui.QBrush(QtGui.QColor('#ffff00')))
					if str(data) == 'подготовка': item.setBackground(QtGui.QBrush(QtGui.QColor('#a7fffd')))
					if str(data) == 'готов': item.setBackground(QtGui.QBrush(QtGui.QColor('#b6d7a8')))
					if str(data) == 'расчёт': item.setBackground(QtGui.QBrush(QtGui.QColor('#4a86e8')))
					if invoice_need and (column_number == 9): item.setBackground(QtGui.QBrush(QtGui.QColor('#f4cccc')))

					self.projectTable.setItem(self.projectTable.rowCount() - 1, column_number, item)

			self.projectTable.setSortingEnabled(True)
			self.projectTable.resizeRowsToContents()

			# обновление списка подстановки в фильтре по партнёру и проекту
			self.partnerCompleter()
			self.projectCompleter()

			self.projectTable.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))

	def filterClear(self):
		self.autoFilter = False
		self.partnerEdit.setText('')
		self.projectNameEdit.setText('')
		for i in range(0, self.filterList.count()):
			self.filterList.item(i).setCheckState(False)
		self.autoFilter = True
		self.tableFill()

	def newProject(self):
		pEdit = ProjectEdit(self)
		pEdit.mode = 'new'
		pEdit.statusComboFill()
		pEdit.partnerComboFill()
		if pEdit.show(): self.tableFill()

	def projectCopy(self):
		try:
			pID = int(self.projectTable.item(self.projectTable.currentItem().row(), 0).text())
		except:
			return
		pCopy = ProjectEdit(self)
		pCopy.projectId = pID
		pCopy.mode = 'new'
		pCopy.recordRead()
		pCopy.deadlineEdit.setDate(QDate.currentDate())
		# pCopy.statusComboBox.setCurrentIndex(0)
		pCopy.invoiceDateEdit.setDate(QDate.currentDate())
		pCopy.invoiceNumberEdit.setText('')
		if pCopy.show():
			currentRow = self.projectTable.currentRow()
			self.tableFill()
			self.projectTable.selectRow(currentRow)

	def statusChange(self, indexes, status_id):
		model = self.projectTable.model()
		role = Qt.DisplayRole
		for index in indexes:
			rec_id = model.data(index, role)
			block_row = queryOne('SELECT TIMESTAMPDIFF (SECOND, (SELECT block_dt FROM projects WHERE id=%s), CURRENT_TIMESTAMP())' % rec_id)
			if (block_row[0] != None) and (block_row[0] < 10):
				block_row = queryOne('select blocker_id, num, project_name from projects where id=%s' % rec_id)
				blocker = queryOne('select firstname, lastname from users where id=%s' % block_row[0])
				msgBox = QtWidgets.QMessageBox()
				msgBox.setWindowTitle('Запись заблокирована.')
				msgBox.setText('Невозможно изменить запись №%s "%s": её редактирует пользователь %s %s' % (block_row[1], block_row[2], blocker[0], blocker[1]))
				msgBox.exec()
			else:
				queryDB('''
						UPDATE projects
						SET
							status_id = %s
						WHERE id = %s
						''', (status_id, rec_id))
		self.tableFill()


	def projectTableMenu(self):
		statuses = query("select `id`, `name`, `order` from project_statuses order by `order`")
		indexes = self.projectTable.selectionModel().selectedRows(column = 0)
		self.menu = QtWidgets.QMenu(self)
		selected = self.projectTable.selectedIndexes()
		if selected:
			projectCopyAction = self.menu.addAction('Создать копию проекта')
			projectCopyAction.triggered.connect(self.projectCopy)
			actdict = {}
			for status in statuses:
				stat = status[0]
				actdict['action%s' % status[0]] = self.menu.addAction('-->' + status[1])
				actdict['action%s' % status[0]].triggered.connect(lambda chk, indexes=indexes, stat=stat: self.statusChange(indexes, stat))
		self.menu.setFont(self.font())
		self.menu.popup(QtGui.QCursor.pos())


def main():
	app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
	loginDialog = LoginDB()
	loginDialog.exec_()
	if loginDialog.connection:
		mainWindow = App()
		mainWindow.show()  # Показываем окно
		app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
	main()  # то запускаем функцию main()
