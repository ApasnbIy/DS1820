# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QMainWindow, QTableWidgetItem
import Main_window_DS1820

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import time

class MAINWindow(QMainWindow, Main_window_DS1820.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.type = "slave"  # необходимо для проерки на вид вызова окна - главное/дочернее
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
        #self.toolbar = NavigationToolbar(self.canvas, self)
        # data
        self.data = {}
        self.pause = 0
        # set the layout

        #
        #self.restartButton.clicked.connect(self.plot)
        #self.pauseButton.toggled.connect(self.pause_set_clr)

    def pause_set_clr(self, checked):
        if checked:
            self.pause = 1
        else:
            self.pause = 0

    def form_table_widget(self):
        try:
            pass


        except Exception as error:
            print(error)





    def plot(self, data=None, show_key_list=None):
        #print(data)
        try:

            self.data = data
            self.show_dict = show_key_list
            name = []
            data_axis = []

            # отрисуем график
            # instead of ax.hold(False)
            self.figure.clear()
            # create an axis
            axes = self.figure.add_subplot(111)
            if self.data:
                self.keys_list = list(self.data.keys())
                #print(self.keys_list)
                self.keys_list.remove('Time')


                for j in self.keys_list:
                    if self.show_dict.get(j):
                        axes.plot(self.data.get('Time'), self.data.get(j), line_type_from_index(self.keys_list.index(j)), label=j)
                    else:
                        pass
                axes.legend()






            else:
                pass
                '''
                #self.data = []
                name = ["Test", "Test2"]
                data_x = [[0, 1, 2, 3], [0, 0.5, 2, 6]]
                data_y = [[0, 1, 4, 9], [9, 4, 1, 45]]
                [axes.plot(data_x[i], data_y[i], line_type_from_index(i), label=name[i]) for i in range(len(name))]
                '''


            # plot data

            axes.set_title("Температура")
            axes.set_ylabel("Температура °C")
            axes.set_xlabel("Время, с")
            axes.grid()

            # refresh canvas
            self.canvas.draw()
        except Exception as error:
            print(error)
        # заполним таблицу
        '''
        self.tableWidget.setRowCount(len(self.data) + 1)
        time_name_item = QTableWidgetItem("Время")
        self.tableWidget.setItem(0, 1, time_name_item)
        time_item = QTableWidgetItem("NA")  # "{:.3g}".format(data_x[0][-1]))
        self.tableWidget.setItem(0, 2, time_item)
        for row in range(len(self.data)):
            for column in range(1, 3):
                if column == 1:
                    table_item = QTableWidgetItem(name[row])
                elif column == 2:
                    try:
                        table_item = QTableWidgetItem("{:.3g}".format(data_y[row][-1]))
                    except IndexError:
                        table_item = QTableWidgetItem("NA")
                else:
                    table_item = QTableWidgetItem("NA")
                self.tableWidget.setItem(row, column, table_item)
        '''



    # Переопределение метода closeEvent, для перехвата события закрытия окна
    def closeEvent(self, event):
        #if self.type == "master":
        #    event.ignore()
        #else:
        self.hide()


def line_type_from_index(n):
    color_line = ["b", "r", "g", "c", "m", "y", "k", "b", "r", "g", "c", "m", "y", "k", "b", "r", "g", "c", "m", "y", "k"]
    style_line = ["-", "--", "-.", ":", ".", ",", "^", "o", "1", "2", "3", "4", "s", "p", "*", "d"]
    try:
        color = color_line[n % len(color_line)]
        style = style_line[n // len(style_line)]
        # print(n % len(color_line), n // len(color_line))
        return style + color
    except Exception:
        return "-r"


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MAINWindow()
    main.pause_set_clr(0)
    #main.plot([['краказябра'], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10], [2.4, 2.2, 2.6, 2.4, 2.2, 2.6, 2.4, 2.2, 2.6, 2.7, 2.6]])
    main.type = "master"
    main.show()
    sys.exit(app.exec_())