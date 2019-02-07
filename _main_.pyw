from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QTableWidgetItem
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import graph_main
import DS1820_serial
import com_port_Stuyf
import time


class MainWindow(graph_main.MAINWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        # работа с COM-портом и данными с платы
        self.temperature_sensor = com_port_Stuyf.OaiSerial(dev_id=0x01, self_id=0x00)

        # создание и подключение графиков
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.cycle_body)
        #self.connect(self.timer,SIGNAL(timeout()),   )

        # создание второго окна с графиками
        #self.GraphWindow = graph_main.MainWindow()
        #self.GraphButton.clicked.connect(self.graph_window_open)
        #

        #self.pushButton.clicked.connect(self.write_log)
        #self.SetDACButton.clicked.connect(self.set_dac)
        self.pushButton_2.clicked.connect(self.com_open)
        self.pushButton_3.toggled.connect(self.cycle_start_stop)
        self.tableWidget.cellClicked.connect(self.cell_clicked)

        self.previos_sensors_numbers = 0
        self.show_dictionary = {}

        layout = QVBoxLayout()
        # layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.graphicsView.setLayout(layout)

        self.newfile()
        #self.pushButton_4.clicked.connect(self.plot)

    def newfile(self):
        self.f1 = open('Logs\\Log_file' + time.strftime("%Y_%m_%d %H-%M-%S", time.localtime()) + ".txt", 'w')
        self.f1_name = self.f1.name
        self.f1.close()




    def cycle_start_stop(self, checked):

        if checked:

            self.pushButton_3.setStyleSheet('QPushButton {background-color: seagreen;}')
            self.timer.start(1000)
        else:
            self.pushButton_3.setStyleSheet('QPushButton {background-color: gray;}')
            self.timer.stop()
        pass

    def cycle_body(self):
        self.get_temperature()
        #self.fill_data_table()
        self.state_check()
        pass

    def tab_click_event(self):

        pass



    def redrow_table_widget(self):
        try:
            if  self.previos_sensors_numbers != self.temperature_sensor.sensors_numbers:
                self.previos_sensors_numbers = self.temperature_sensor.sensors_numbers
                self.tableWidget.setRowCount(self.temperature_sensor.sensors_numbers)

                for i in range(self.temperature_sensor.sensors_numbers):
                    #btn = QtWidgets.QCheckBox(self.tableWidget)
                    #self.tableWidget.setCellWidget(i, 0, btn)
                    self.tableWidget.setItem(i, 1, QTableWidgetItem( '%d' %(self.temperature_sensor.sensors_serial_numbers[i])))
                    self.show_dictionary.update({self.temperature_sensor.sensors_serial_numbers[i]: True})

                    self.tableWidget.setItem(i, 2, QTableWidgetItem())
                    self.tableWidget.setItem(i, 0, QTableWidgetItem())
                    self.tableWidget.item(i, 0).setBackground(QtGui.QColor("palegreen"))
            else:
                pass

        except Exception as error:
            print(error)
        pass

    def cell_clicked(self, row, column):
        try:
            if(column == 0):
            #self.tableWidget.setItem(row, column, self.tableWidget.item(row, column))
                if self.show_dictionary.get(int(self.tableWidget.item(row,1).text())):
                    self.show_dictionary.update({int(self.tableWidget.item(row,1).text()):False})
                    self.tableWidget.item(row, column).setBackground(QtGui.QColor("lightcoral"))
                else:
                    self.tableWidget.item(row, column).setBackground(QtGui.QColor("palegreen"))
                    self.show_dictionary.update({int(self.tableWidget.item(row, 1).text()): True})
            else:
                pass
            #print("Row %d and Column %d was clicked" % (row, column))
        except Exception as error:
            pass
        pass


    def write_to_file(self):
        f1 = open(self.f1_name, "a")
        keys = self.temperature_sensor.temperature_pars_data.keys()

        if(keys):
            for key in keys:
                f1.write("\t" + str(key) + "\t" + str(self.temperature_sensor.temperature_pars_data.get(key)[-1]) + "\t")
            f1.write("\n")
            f1.close()
        else:
            pass

    def get_temperature(self):
        self.temperature_sensor.request(req_type="get_temperature")
        data = self.temperature_sensor.temperature_pars_data
        self.redrow_table_widget()
        self.plot(data, self.show_dictionary)
        try:
            self.write_to_file()
            for j in range(self.temperature_sensor.sensors_numbers):
                self.tableWidget.item(j, 2).setText('%.3f' % (data.get(int(self.tableWidget.item(j, 1).text()))[-1]))

        except Exception as error:
            print(error)
            pass

        #data.clear()

        #print(self.temperature_sensor.temperature_pars_data)
        #self.fill_data_table()
        #self.state_check()
        pass
    '''
    def set_dac(self):
        data = int(self.DACEntry.text())
        self.temperature_sensor.request(req_type="set_dac", data=[(data >> 8) & 0xFF, (data >> 0) & 0xFF])
        self.fill_data_table()
        self.state_check()
        pass
    '''
    def fill_data_table(self):
        data = self.temperature_sensor.temperature_pars_data
        #print(self.temperature_sensor.temperature_pars_data)
        self.plot(data)
        '''
        self.GraphWindow.plot(self.temperature_sensor.data.graph_data)
        for row in range(len(data)):
            for column in range(len(data[row])):
                table_item = QtWidgets.QTableWidgetItem(data[row][column])
                self.tableWidget.setItem(row, column, table_item)
        pass
        '''

    def com_open(self):
        self.temperature_sensor.serial_numbers = ['A9CBNTXHA']
        if self.temperature_sensor.open_id():
            self.lineEdit_2.setText("Подключение успешно")
            self.pushButton_2.setStyleSheet('QPushButton {background-color: seagreen;}')
        else:
            self.lineEdit_2.setText("Подключение не успешно")
            self.pushButton_2.setStyleSheet('QPushButton {background-color: salmon}')

    def state_check(self):
        if self.temperature_sensor.state:
            self.pushButton_2.setStyleSheet('QPushButton {background-color: seagreen}')
        else:
            self.pushButton_2.setStyleSheet('QPushButton {background-color: salmon}')
        self.lineEdit_2.setText(self.temperature_sensor.error_string)
        pass

    def graph_window_open(self):
        self.GraphWindow.show()

    # Переопределение метода closeEvent, для перехвата события закрытия окна
    #def closeEvent(self, event):
     #   self.GraphWindow.close()




if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = MainWindow()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()  # и запускаем приложение