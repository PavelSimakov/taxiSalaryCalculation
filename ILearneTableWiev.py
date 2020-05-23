from PyQt5 import QtWidgets, QtGui, QtCore

import MainForm


class MyWindow(QtWidgets.QMainWindow, MainForm.Ui_mainWindow):
    def __init__(self, master=None):
        QtWidgets.QMainWindow.__init__(self, master)
        self.setupUi(self)

        self.date = QtCore.QDate
        self.dateEdit_shiftSelected.setDate(self.date.currentDate())

        self.shiftVerticalHeaderList = ('Яндекс', 'Gett', 'City', 'Общий накат', 'Какой процент', 'Мой процент',
                                        'Штрафы', 'За смену')
        self.shiftsNameList = []
        self.shiftDateList = []
        self.dateMonth = {}

        self.settingHHeaderList = ['Накат', 'Процент']
        self.settingDateDict = {}
        self.settingTariffList = [{}] * 4
        print(self.settingTariffList)

        self.comboBox_selectTariff.setItemData(0, self.settingTariffList[0])
        self.comboBox_selectTariff.setItemData(1, self.settingTariffList[1])
        self.comboBox_selectTariff.setItemData(2, self.settingTariffList[2])
        self.comboBox_selectTariff.setItemData(3, self.settingTariffList[3])

        self.StIM_settingTable = QtGui.QStandardItemModel()
        self.StIM_settingTable.setHorizontalHeaderLabels(self.settingHHeaderList)
        self.tableView_settingTariff.setModel(self.StIM_settingTable)
        self.StIM_shiftsTable = QtGui.QStandardItemModel()
        self.StIM_shiftsTable.setVerticalHeaderLabels(self.shiftVerticalHeaderList)
        self.tableView_shifts.setModel(self.StIM_shiftsTable)

        self.action_addRow.triggered.connect(self.addRow_setting)
        self.action_removeRow.triggered.connect(self.removeRow_setting)
        self.action_saveSetting.triggered.connect(self.saveSetting)
        self.action_saveTariff.triggered.connect(self.saveTariff)
        self.action_addShift.triggered.connect(self.addShift_tableShifts)
        self.action_calculatedShift.triggered.connect(self.calculatedShift)

    def addRow_setting(self):
        L = []
        for i in range(0, 2):
            L.append(QtGui.QStandardItem('0'))
        self.StIM_settingTable.appendRow(L)

    def removeRow_setting(self):
        index = self.tableView_settingTariff.currentIndex()
        if index.isValid():
            self.StIM_settingTable.removeRow(index.row())

    def addShift_tableShifts(self):
        L = []
        self.shiftsNameList.append(self.dateEdit_shiftSelected.text())
        for i in range(0, 8):
            L.append(QtGui.QStandardItem('0'))
        self.StIM_shiftsTable.appendColumn(L)
        self.StIM_shiftsTable.setHorizontalHeaderLabels(self.shiftsNameList)

    def calculatedShift(self):
        ind = self.tableView_shifts.currentIndex()
        sel = self.tableView_shifts.selectionModel()
        if sel.isRowSelected(ind.row(), QtCore.QModelIndex()):
            fullSalary = sum([float(self.StIM_shiftsTable.index(0, ind.column()).data(QtCore.Qt.EditRole)), float(
                self.StIM_shiftsTable.index(1, ind.column()).data(QtCore.Qt.EditRole)), float(
                self.StIM_shiftsTable.index(2, ind.column()).data(QtCore.Qt.EditRole))])
            item = QtGui.QStandardItem(str(fullSalary))
            self.StIM_shiftsTable.setItem(3, ind.column(), item)
            print(fullSalary)

    def saveSetting(self):
        pass

    def saveTariff(self):
        key_list = []
        date_list = []
        name_tariff = self.comboBox_selectTariff.currentIndex()
        ind = QtCore.QModelIndex()
        for i in range(0, self.StIM_settingTable.rowCount(ind)):
            key_list.append(float(self.StIM_settingTable.index(i, 0).data()))
            date_list.append(float(self.StIM_settingTable.index(i, 1).data()))
        self.settingDateDict = dict(zip(key_list, date_list))
        self.settingTariffList[name_tariff] = self.settingDateDict


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
