# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\edit_project.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(921, 760)
        font = QtGui.QFont()
        font.setPointSize(10)
        Dialog.setFont(font)
        Dialog.setStyleSheet("")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.newPartnerButton = QtWidgets.QPushButton(Dialog)
        self.newPartnerButton.setObjectName("newPartnerButton")
        self.horizontalLayout.addWidget(self.newPartnerButton)
        self.infoPartnerButton = QtWidgets.QPushButton(Dialog)
        self.infoPartnerButton.setObjectName("infoPartnerButton")
        self.horizontalLayout.addWidget(self.infoPartnerButton)
        spacerItem = QtWidgets.QSpacerItem(27, 25, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.buttonBox.setFont(font)
        self.buttonBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.buttonBox.setStyleSheet("font-size: 10pt")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout.addWidget(self.buttonBox)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.formLayout_6 = QtWidgets.QFormLayout()
        self.formLayout_6.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_6.setObjectName("formLayout_6")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.partnerComboBox = ExtendedComboBox(Dialog)
        self.partnerComboBox.setMaxVisibleItems(30)
        self.partnerComboBox.setObjectName("partnerComboBox")
        self.formLayout_6.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.partnerComboBox)
        self.horizontalLayout_3.addLayout(self.formLayout_6)
        self.formLayout_7 = QtWidgets.QFormLayout()
        self.formLayout_7.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_7.setObjectName("formLayout_7")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.deadlineEdit = QtWidgets.QDateEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.deadlineEdit.setFont(font)
        self.deadlineEdit.setMinimumDate(QtCore.QDate(1900, 1, 1))
        self.deadlineEdit.setCalendarPopup(True)
        self.deadlineEdit.setObjectName("deadlineEdit")
        self.formLayout_7.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.deadlineEdit)
        self.horizontalLayout_3.addLayout(self.formLayout_7)
        self.formLayout_8 = QtWidgets.QFormLayout()
        self.formLayout_8.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_8.setObjectName("formLayout_8")
        self.label_10 = QtWidgets.QLabel(Dialog)
        self.label_10.setObjectName("label_10")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.statusComboBox = QtWidgets.QComboBox(Dialog)
        self.statusComboBox.setObjectName("statusComboBox")
        self.formLayout_8.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.statusComboBox)
        self.horizontalLayout_3.addLayout(self.formLayout_8)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.formLayout_9 = QtWidgets.QFormLayout()
        self.formLayout_9.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_9.setObjectName("formLayout_9")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.projectNameEdit = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.projectNameEdit.setFont(font)
        self.projectNameEdit.setObjectName("projectNameEdit")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.projectNameEdit)
        self.verticalLayout_2.addLayout(self.formLayout_9)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.formLayout_3 = QtWidgets.QFormLayout()
        self.formLayout_3.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.quantitySpinBox = QtWidgets.QSpinBox(Dialog)
        self.quantitySpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.quantitySpinBox.setProperty("showGroupSeparator", False)
        self.quantitySpinBox.setMinimum(1)
        self.quantitySpinBox.setMaximum(999999999)
        self.quantitySpinBox.setProperty("value", 1)
        self.quantitySpinBox.setObjectName("quantitySpinBox")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.quantitySpinBox)
        self.horizontalLayout_2.addLayout(self.formLayout_3)
        self.formLayout_4 = QtWidgets.QFormLayout()
        self.formLayout_4.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_4.setObjectName("formLayout_4")
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setObjectName("label_11")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_11)
        self.priceSpinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.priceSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.priceSpinBox.setProperty("showGroupSeparator", False)
        self.priceSpinBox.setMaximum(9999999999999.99)
        self.priceSpinBox.setObjectName("priceSpinBox")
        self.formLayout_4.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.priceSpinBox)
        self.horizontalLayout_2.addLayout(self.formLayout_4)
        self.formLayout_5 = QtWidgets.QFormLayout()
        self.formLayout_5.setObjectName("formLayout_5")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.amountSpinBox = QtWidgets.QDoubleSpinBox(Dialog)
        self.amountSpinBox.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.amountSpinBox.setProperty("showGroupSeparator", False)
        self.amountSpinBox.setMaximum(9999999999999.99)
        self.amountSpinBox.setObjectName("amountSpinBox")
        self.formLayout_5.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.amountSpinBox)
        self.horizontalLayout_2.addLayout(self.formLayout_5)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.formLayout_10 = QtWidgets.QFormLayout()
        self.formLayout_10.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_10.setObjectName("formLayout_10")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setObjectName("label_7")
        self.formLayout_10.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.folderEdit = QtWidgets.QLineEdit(Dialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.folderEdit.setFont(font)
        self.folderEdit.setObjectName("folderEdit")
        self.formLayout_10.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.folderEdit)
        self.verticalLayout_2.addLayout(self.formLayout_10)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.invoiceNeedCheckBox = QtWidgets.QCheckBox(Dialog)
        self.invoiceNeedCheckBox.setChecked(True)
        self.invoiceNeedCheckBox.setObjectName("invoiceNeedCheckBox")
        self.horizontalLayout_4.addWidget(self.invoiceNeedCheckBox)
        self.formLayout_2 = QtWidgets.QFormLayout()
        self.formLayout_2.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.invoiceNumberEdit = QtWidgets.QLineEdit(Dialog)
        self.invoiceNumberEdit.setObjectName("invoiceNumberEdit")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.invoiceNumberEdit)
        self.horizontalLayout_4.addLayout(self.formLayout_2)
        self.horizontalLayout_5.addLayout(self.horizontalLayout_4)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setLabelAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.formLayout.setFormAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTop|QtCore.Qt.AlignTrailing)
        self.formLayout.setObjectName("formLayout")
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setObjectName("label_9")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.invoiceDateEdit = QtWidgets.QDateEdit(Dialog)
        self.invoiceDateEdit.setAccelerated(True)
        self.invoiceDateEdit.setProperty("showGroupSeparator", False)
        self.invoiceDateEdit.setDateTime(QtCore.QDateTime(QtCore.QDate(2000, 1, 1), QtCore.QTime(0, 0, 0)))
        self.invoiceDateEdit.setCalendarPopup(True)
        self.invoiceDateEdit.setObjectName("invoiceDateEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.invoiceDateEdit)
        self.horizontalLayout_5.addLayout(self.formLayout)
        self.addPayButton = QtWidgets.QPushButton(Dialog)
        self.addPayButton.setObjectName("addPayButton")
        self.horizontalLayout_5.addWidget(self.addPayButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout_5)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.splitter = QtWidgets.QSplitter(self.groupBox)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.commentBrowser = QtWidgets.QTextBrowser(self.splitter)
        self.commentBrowser.setOpenExternalLinks(False)
        self.commentBrowser.setOpenLinks(False)
        self.commentBrowser.setObjectName("commentBrowser")
        self.commentsEdit = QtWidgets.QTextEdit(self.splitter)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.commentsEdit.sizePolicy().hasHeightForWidth())
        self.commentsEdit.setSizePolicy(sizePolicy)
        self.commentsEdit.setReadOnly(False)
        self.commentsEdit.setObjectName("commentsEdit")
        self.verticalLayout.addWidget(self.splitter)
        self.verticalLayout_2.addWidget(self.groupBox)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept) # type: ignore
        self.buttonBox.rejected.connect(Dialog.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.partnerComboBox, self.deadlineEdit)
        Dialog.setTabOrder(self.deadlineEdit, self.statusComboBox)
        Dialog.setTabOrder(self.statusComboBox, self.projectNameEdit)
        Dialog.setTabOrder(self.projectNameEdit, self.quantitySpinBox)
        Dialog.setTabOrder(self.quantitySpinBox, self.priceSpinBox)
        Dialog.setTabOrder(self.priceSpinBox, self.amountSpinBox)
        Dialog.setTabOrder(self.amountSpinBox, self.folderEdit)
        Dialog.setTabOrder(self.folderEdit, self.invoiceNumberEdit)
        Dialog.setTabOrder(self.invoiceNumberEdit, self.invoiceDateEdit)
        Dialog.setTabOrder(self.invoiceDateEdit, self.commentsEdit)
        Dialog.setTabOrder(self.commentsEdit, self.newPartnerButton)
        Dialog.setTabOrder(self.newPartnerButton, self.infoPartnerButton)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Заявка/продажа"))
        self.newPartnerButton.setText(_translate("Dialog", "Новый партнёр"))
        self.infoPartnerButton.setText(_translate("Dialog", "Инф. о партнёре"))
        self.label_2.setText(_translate("Dialog", "партнёр"))
        self.label_6.setText(_translate("Dialog", "срок"))
        self.label_10.setText(_translate("Dialog", "статус"))
        self.label_3.setText(_translate("Dialog", "наименование"))
        self.label_4.setText(_translate("Dialog", "количество"))
        self.label_11.setText(_translate("Dialog", "цена"))
        self.label_5.setText(_translate("Dialog", "сумма"))
        self.label_7.setText(_translate("Dialog", "путь к рабочим файлам"))
        self.invoiceNeedCheckBox.setText(_translate("Dialog", "выставить"))
        self.label_8.setText(_translate("Dialog", "номер счёта"))
        self.label_9.setText(_translate("Dialog", "дата счёта"))
        self.addPayButton.setText(_translate("Dialog", "Добавить платёж"))
        self.groupBox.setTitle(_translate("Dialog", "описание"))
        self.commentBrowser.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.commentsEdit.setPlaceholderText(_translate("Dialog", "Написать комментарий."))
from completer import ExtendedComboBox
