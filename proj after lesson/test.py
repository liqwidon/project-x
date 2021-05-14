#!/usr/bin/env python
# coding: utf-8

# # Визуализация результатов работы генетического алгоритма в терминах поиска экстремума

# ### ПОДКЛЮЧЕНИЕ ИСПОЛЬЗУЕМЫХ БИБЛИОТЕК

# In[11]:


import sys

import random as rd
#для использования union при кроссинговере
from ctypes import *

#две библиотеки для работы с битсетами
from bitarray import bitarray
import bitstring

#графика
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

import matplotlib.pyplot as plt
import numpy as np
import numexpr as ne

from mpl_toolkits import mplot3d
from mpl_toolkits.mplot3d import Axes3D


# # РОДИТЕЛЬСКИЙ КЛАСС

# In[12]:


#Модуль написал Ревошин М.С.
#Дата написания 10.04.2021
#Дата финальной доработки 13.05.2021
#Отладка Морозов А.Т.

class Window(QMainWindow):
    #отслеживание перезапуска
    EXIT_CODE_REBOOT = -123
    def __init__(self, ui):
        super(Window,self).__init__()
        self.ui = uic.loadUi(ui, self)
        self.setFixedSize(self.geometry().width(),self.geometry().height())
        
        self.click()
    
    def SetWidget(self):
        self.figure = plt.Figure()
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.toolbar)
        self.w1.setLayout(layout)
        self.ax = self.figure.add_subplot(1, 1, 1)
    
    def SetWidget3D(self):
        self.figure2 = plt.Figure()
        self.canvas2 = FigureCanvas(self.figure2)
        self.toolbar2 = NavigationToolbar(self.canvas2, self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas2)
        layout.addWidget(self.toolbar2)
        self.w2.setLayout(layout)
        self.ax2 = Axes3D(self.figure2)
    
    def click(self):
        pass
    
    def CreateWindowGraph(self):
        pass
    
    def CheckFormula(self, f):
        if self.inputline.text() == '':
            QMessageBox.critical(self, "Ошибка ", "Не оставляйте поле для ввода пустым)", QMessageBox.Ok)
            return  False
            
        try:
            x = [1, 4, 5]
            z = ne.evaluate(f)
        except KeyError:
            try:
                x = [1, 4, 5]
                y = [1, 5, 7]
                z = ne.evaluate(f)
            except ValueError:
                QMessageBox.critical(self, "Ошибка-формула", "Формула не может иметь '1 измерение'", QMessageBox.Ok)
                return False
            except KeyError:
                QMessageBox.critical(self, "Ошибка-формула", "Неопознанные переменные в формуле", QMessageBox.Ok)
                return False
            except SyntaxError:
                QMessageBox.critical(self, "Ошибка-формула", "Неправильная формула", QMessageBox.Ok)
                return False
            return True
        except SyntaxError:
            QMessageBox.critical(self, "Ошибка-формула", "Неправильная формула", QMessageBox.Ok)
            return False
        
        try:
            x = [1, 4, 5]
            self.ax.plot(x,ne.evaluate(f))
        except ValueError:
            QMessageBox.critical(self, "Ошибка-формула", "Формула не может иметь '1 измерение'", QMessageBox.Ok)
            return False
        
        return True
    
    def SetDimentions(self, formula):
        try:
            x = [1, 4, 5]
            z = ne.evaluate(formula)
        except KeyError:
            return True
        return False
    
    def PrintFormula(self, *args):
        if len(args) < 6:
            try:
                x = np.arange(float(args[0]), float(args[1]), float(args[2]))
            except ValueError:
                QMessageBox.critical(self, "Ошибка-переменные", "Неправильные параметры 'x'", QMessageBox.Ok)
                return
            except ZeroDivisionError:
                QMessageBox.critical(self, "Ошибка-переменные", "Неподходящий диапазон 'x'", QMessageBox.Ok)
                return
            except SyntaxError:
                QMessageBox.critical(self, "Ошибка-переменные", "Неверная формула", QMessageBox.Ok)
                return
        
            self.w1.setVisible(True)
            y = ne.evaluate(args[3])
            self.ax.grid(True)
            self.ax.plot(x, y)
            self.SetWidgetTrue()
        else:
            if float(args[4]) <= 1:
                QMessageBox.critical(self, "Ошибка-переменные", "Выберите d >=1", QMessageBox.Ok)
                return
            try:
                x = np.arange(float(args[0]), float(args[1]),
                             np.abs((float(args[0]) - float(args[1])) / float(args[4])))
                y = np.arange(float(args[2]), float(args[3]),
                             np.abs((float(args[2]) - float(args[3])) / float(args[4])))
            except ValueError:
                QMessageBox.critical(self, "Ошибка-переменные", "Неправильные параметры 'x/y'", QMessageBox.Ok)
                return
            except ZeroDivisionError:
                QMessageBox.critical(self, "Ошибка-переменные", "Неподходящий диапазон 'x/y'", QMessageBox.Ok)
                return
            except SyntaxError:
                QMessageBox.critical(self, "Ошибка-переменные", "Неверная формула", QMessageBox.Ok)
                return
            
            
            if self.cb_graph.isChecked():
                x, y = np.meshgrid(x, y)
                
                self.surf = self.ax2.plot_surface(x, y, ne.evaluate(args[5]), cmap = plt.cm.coolwarm,
                                                      linewidth = 0, antialiased = False)
                self.w2.setVisible(True)
                    
            else:
                x, y = np.meshgrid(x, y)
                self.ax.contourf(x, y, ne.evaluate(args[5]))
                self.w1.setVisible(True)
            self.SetWidgetTrue()
            
    
    def PrintInput(self, args):
        pass
    
    def PrintFile(self, file):
        pass
    
    def Reset(self):
        qApp.exit( Window.EXIT_CODE_REBOOT )


# #### ГЛАВНЫЙ ИНТЕРФЕЙС

# In[13]:


#Модуль написал Ревошин М.С.
#Дата написания 20.04.2021
#Дата финальной доработки 13.05.2021
#Отладка и проверка Морозов А.Т.

class MainWindow(Window):
    def __init__(self):
        Window.__init__(self, ui = 'mainwindow.ui')
        
        self.inputline_2.setVisible(False)
        self.lineEdit_2.setVisible(False)
        
        self.SetWidget()
        self.w1.setVisible(False)
        
    def click(self):
        self.exit.clicked.connect(lambda: self.close())
        
        self.cb_i.clicked.connect(lambda: self.ChangeInput())
        self.cb_w.clicked.connect(lambda: self.ChangeInputWay())
        self.cb_f.clicked.connect(lambda: self.ChangeInputForm())
        self.b_f.clicked.connect(lambda: self.CreateWindowGraph())
        self.b_e.clicked.connect(lambda: self.CreateExtremGraph())
        
        self.reset.clicked.connect(lambda: self.Reset())
        
    def CheckBox(self):
        if self.cb_w.isChecked()and self.cb_i.isChecked():
            return False
        if self.cb_f.isChecked() == True and self.cb_i.isChecked() == True:
            return False
        if self.cb_f.isChecked() == True and self.cb_w.isChecked() == True:
            return False
        
        return True
    
    def ChangeInputForm(self):
        if self.CheckBox() == True:
            return
        else: 
            self.cb_f.setChecked(False)
            
    def ChangeInputWay(self):
        if self.CheckBox() == True:
            if self.cb_w.isChecked() == True:
                self.lineEdit.setText('Путь : ')
            else:
                self.lineEdit.setText('f(x) = ')
        else: 
            self.cb_w.setChecked(False)
        
    def ChangeInput(self):
        if self.CheckBox() == True:
            if self.cb_i.isChecked() == True:
                self.inputline_2.setVisible(True)
                self.lineEdit_2.setVisible(True)
                self.lineEdit.setText('Y = ')
            else: 
                self.inputline_2.setVisible(False)
                self.lineEdit_2.setVisible(False)
                self.lineEdit.setText('f(x) = ')
        else:
            self.cb_i.setChecked(False)
        
    def CreateExtremGraph(self):
        if self.CheckFormula(self.inputline.text()) == False:
            return
        if self.CheckBox() == True:
            if self.cb_f.isChecked() == True:
                self.w = WindowExtremum('formula', self.inputline.text())
                self.w.show()
                
            elif self.cb_w.isChecked() == True:
                self.w = WindowExtremum(['file', self.inputline.text()])
                self.w.show()
        
    def CreateWindowGraph(self):
        if self.CheckFormula(self.inputline.text()) == False:
            return
        if self.CheckBox() == True:
            if self.cb_f.isChecked() == True:
                self.w = WindowGraph(['formula',self.inputline.text()])
                self.w.show()


# #### ИНТЕРФЕЙС ГРАФИКОВ(с формулы/входных данных/с файла)

# In[14]:


#Автор Ревошин М.С.
#Дата написания 23.04.2021
#Дата доработки 13.05.2021
#Проверил Морозов А.Т.

class WindowGraph(Window):
    def __init__(self, argv):
        inputType = argv[0]
        Window.__init__(self, 'graph.ui')
        self.SetWidget()
        self.SetWidget3D()
        
        self.isMulti = False
        formula = argv[1]
        if self.SetDimentions(formula):
            self.isMulti = True
        
        if (inputType == 'formula'):
            
            self.formula.setText(formula)
            self.SetWidgetFalse()

        
    def SetWidgetFalse(self):
        
        self.w1.setVisible(False)
        self.w2.setVisible(False)
        
        self.back.setVisible(False)
        self.cb_graph.setVisible(False)
        
        self.show_g.setVisible(True)
        
        self.minX.setVisible(True)
        self.maxX.setVisible(True)
        self.stepX.setVisible(True)
        
        self.minLX.setVisible(True)
        self.maxLX.setVisible(True)
        self.stepLX.setVisible(True)
        
        self.minY.setVisible(False)
        self.maxY.setVisible(False)
        
        self.minLY.setVisible(False)
        self.maxLY.setVisible(False)
        
        if self.isMulti:
            self.stepX.setText("Шаг")
            self.cb_graph.setVisible(True)
            
            self.minY.setVisible(True)
            self.maxY.setVisible(True)
        
            self.minLY.setVisible(True)
            self.maxLY.setVisible(True)
        
        self.ax.clear()
        self.ax2.clear()
    
    def SetWidgetTrue(self):
        
        self.show_g.setVisible(False)
        self.cb_graph.setVisible(False)
        
        self.minX.setVisible(False)
        self.maxX.setVisible(False)
        self.stepX.setVisible(False)
        
        self.minLX.setVisible(False)
        self.maxLX.setVisible(False)
        self.stepLX.setVisible(False)
        
        self.minY.setVisible(False)
        self.maxY.setVisible(False)
        
        self.minLY.setVisible(False)
        self.maxLY.setVisible(False)
        
        self.back.setVisible(True)
    
    def Print(self):
        if self.isMulti:
            self.PrintFormula(self.minLX.text(), self.maxLX.text(), self.minLY.text(),
                              self.maxLY.text(), self.stepLX.text(), self.formula.text())
        else: 
            self.PrintFormula(self.minLX.text(), self.maxLX.text(), self.stepLX.text(), self.formula.text())
    
    def click(self):
        self.show_g.clicked.connect(lambda: self.Print())
        
        self.back.clicked.connect(lambda: self.SetWidgetFalse())
        
        self.cb_graph.stateChanged.connect(lambda: self.ChangeOutput())
    
    def ChangeOutput(self):
        if self.cb_graph.isChecked():
            self.cb_graph.setText('3д график')
        else:
            self.cb_graph.setText('Градиент')
    
    def PrintFile(self, file):
        self.SetWidgetTrue()
        self.back.setVisible(False)
        
    def PrintInput(self, args):
        self.x, self.y = args[0], args[1]
        self.SetWidgetTrue()
        self.back.setVisible(False)
        self.lineEdit_3.setVisible(False)
        self.formula.setVisible(False)
        
        self.ax.grid(True)
        try:
            self.ax.plot(self.x, self.y)
        except ValueError:
            QMessageBox.critical(self, "Ошибка ", "Несовпадение размеров 'x' и 'y'", QMessageBox.Ok)
            self.deleteLater()
            return


# #### РАСЧЁТ ЭКСТРЕМУМА

# In[15]:


#Написал Морозов А.Т.
#Дата написания 01.04.2021 - 01.05.2021
#Дата финальной доработки 14.05.2021
#Проверил Ревошин М.С.

#Основной класс генетического алгоритма
class GeneticAlgorithm():
    
    def __init__(self, pop_c, formula):
        self.x_min = -100
        self.x_max = 100
        self.z_min = -100
        self.z_max = 100
        self.formula = formula
        self.mutation_probability = 0   #вероятность мутации, возможность мутация может быть добавлена
        self.population_count  = pop_c  #население
        self.cross_probability = 1   #вероятность скрещивания
                
        step_x = (self.x_max - self.x_min) / self.population_count  #шаг по оси х
        step_z = (self.z_max - self.z_min) / self.population_count  #шаг по оси y
         
        self.data = []       #храним пары [x, z] координат
        self.res  = []       #храним результаты функции

        #заполняем data и res
        for idx in range(0, self.population_count):
            self.data.append([self.x_min + step_x * idx, self.z_min + step_z * idx]);
            self.res.append(self.function(self.data[idx][0], self.data[idx][1]));
    
    #метод турнирного отбора, с помощью которой выбирается пара точек, сравнивается и победитель сохраняется, а проигравший дерется еще раз
    def tournamentSelection(self):
        buff = []
        rb   = []

        while len(buff) != self.population_count:
            t1 = rd.randint(0, 10000) % len(self.data)
            t2 = rd.randint(0, 10000) % len(self.data)

            if self.res[t1] > self.res[t2]:
                buff.append(self.data[t1])
                rb.append(self.res[t1])

                #аналог std::swap
                self.data[t1], self.data[-1] = self.data[-1], self.data[t1] 
                self.res[t1],  self.res[-1]  = self.res[-1],  self.res[t1]
                self.data.pop()
                self.res.pop()
            else:
                buff.append(self.data[t2])
                rb.append(self.res[t2])

                self.data[t2], self.data[-1] = self.data[-1], self.data[t2] 
                self.res[t2],  self.res[-1]  = self.res[-1],  self.res[t2]
                self.data.pop()
                self.res.pop()

        self.data = buff
        self.res  = rb
        
        #При вводе вручную функция задается здеся
    def function(self, x, y):
#         return float(-(x * x + z * z))
        return float(ne.evaluate(self.formula))

    #Функция, которая должна! "убивать" детей, которые не подходят нашим условиям
    def kill(self, c1, c2):
        if c1[0] > self.x_max or c1[0] < self.x_min or c1[1] > self.z_max or c1[1] < self.z_min or c2[0] > self.x_max or c2[0] < self.x_min or c2[1] > self.z_max or c2[1] < self.z_min:
            return True
        else:
            return False
    
    #Поиск лучших кондидатов после кроссинговера для селекции
    def searchBest(self):
        color = [False] * len(self.data)       #закрашиваем тех, кого скрестили
                                               #используем случайный выбор для кроссинговера
        for k in range(0, self.population_count):
            j = rd.randint(0, 100000) % self.population_count
            i = rd.randint(0, 100000) % self.population_count

            if color[i] == False:
                b1 = self.data[j]
                b2 = self.data[i]
                self.crossingOver(b1, b2)
                if self.kill(b1, b2):
                    self.data.append(b1)
                    self.data.append(b2)
                    self.res.append(self.function(b1[0], b1[1]))
                    self.res.append(self.function(b2[0], b2[1]))
            
                color[i] = True
                color[j] = True
        #после скрещивания надо провести отбор
        self.tournamentSelection()
    
    #БЛОК В РАЗРАБОТКЕ
    #Мутации, должны менять случайно значения испытуемых чтобы в случае тупика выбраться из него
    def mutation(self, c):
        class actual_data( Union ):
            _fields_ = [( "in_", c_float ), ( 'out_', c_ulong )]
        uni = actual_data()

        uni.in_ = c
        f1 = bitstring.BitArray(float = uni.out_, length = 32) 
        bi = f1.bin
        a = bitarray(bi)

        pred = rd.randint(0, 100000) % 1000 / 1000;

        if pred < self.mutation_probability:
            idx = rd.randint(0, 100000) % 31
            a[idx] = 0 if (a[idx] == 1) else 1
            uni.out_ = int(a.to01(), 2)

        return uni.in_
    
    #Кроссинговер
    def crossingOver(self, cop_1, cop_2):
        #Для каждой координаты производин смешивание генов с использованием Union и битовых масок
        for i in 0, 1:
            class actual_data( Union ):
                _fields_ = [( "in_", c_float ), ( 'out_', c_ulong )]
            uni_1 = actual_data()
            uni_2 = actual_data()
            
            uni_1.in_ = cop_1[i]
            uni_2.in_ = cop_2[i]

            f1 = bitstring.BitArray(float = uni_1.in_, length = 32) 
            bi1 = f1.bin
            bits_1 = bitarray(bi1)
            bits_1_buff = bitarray(bi1)
            
            f2 = bitstring.BitArray(float = uni_2.in_, length = 32)
            bi2 = f2.bin
            bits_2 = bitarray(bi2)
            bits_2_buff = bitarray(bi2)

            flag = rd.randint(0, 100000) % 31
            for j in range(flag, 0, -1):
                bits_2_buff[j] = bits_1[j]
                bits_1_buff[j] = bits_2[j]
            
            uni_1.out_ = int(bits_1_buff.to01(), 2)
            uni_2.out_ = int(bits_2_buff.to01(), 2)

            
            cop_1[i] = self.mutation(float(uni_1.in_))
            cop_2[i] = self.mutation(float(uni_2.in_))
    
    #получение результата
    def result(self):
        x = 0
        y = 0
        result = -2147483648

        for i in range(0, len(self.data)):
            if self.res[i] > result:
                x = self.data[i][0]
                y = self.data[i][1]
                result = self.res[i]

        return [x, y, result]


# #### ИНТЕРФФЕЙС ЭКСТРЕМУМА

# In[16]:


#Написал Морозов А.Т.
#Написано 10.05.2021
#Проверено 13.05.2021
#Проверял Ревошин М.С.

class WindowExtremum(Window):
    def __init__(self, typeC, arg):
        Window.__init__(self, ui = 'extremum.ui')
        self.SetWidget()
        self.SetWidget3D()
        if typeC == 'formula':
            self.formula.setText(arg)
            self.SetWidgetFalse()
        elif typeC == 'file':
            self.PrintFile(arg)
        
    def SetWidgetFalse(self):
        self.w1.setVisible(False)
        self.w2.setVisible(False)
        self.ax2.clear()
        self.ax.clear()
        
        self.cb_graph.setVisible(True)
        self.back.setVisible(False)
        
        #делаем элементы графики видимыми, они убраны по спискам, чтобы не было нагромаждения
        self.label_list = [self.label, self.label_2, self.label_3, self.label_4, self.label_5, self.label_6, self.label_7]
        for i in self.label_list:
            i.setVisible(True)
            
        self.calcul.setVisible(True)
        
        self.lineEdit_list = [self.lineEdit, self.lineEdit_2, self.lineEdit_4, self.lineEdit_5, 
                              self.lineEdit_6, self.lineEdit_7]
        for i in self.lineEdit_list:
            i.setVisible(True)
            
        self.l_list = [self.l1, self.l2, self.l3, self.l4, self.l5, self.l6, self.l7]
        for i in self.l_list:
            i.setVisible(True)
    
    def SetWidgetTrue(self):
        self.cb_graph.setVisible(False)
        self.back.setVisible(True)
        
        self.label_list = [self.label, self.label_2, self.label_3, self.label_4, self.label_5, self.label_6, self.label_7]
        for i in self.label_list:
            i.setVisible(False)
            
        self.calcul.setVisible(False)
        
        self.l_list = [self.l1, self.l2, self.l3, self.l4, self.l5, self.l6, self.l7]
        for i in self.l_list:
            i.setVisible(False)
    
    def CalculateExtr(self):
        self.PrintFormula(self.l1.text(), self.l2.text(), self.l3.text(), self.l4.text(), self.l5.text(), self.formula.text())
        Extr = GeneticAlgorithm(int(self.l5.text()), self.formula.text())
        for i in range(int(self.l7.text())):
            Extr.searchBest()
        r = Extr.result()
        self.lineEdit.setText(str(r[0]))
        self.lineEdit_5.setText(str(r[1]))
        self.lineEdit_7.setText(str(r[2]))
        
        if self.cb_graph.isChecked():
            self.ax2.scatter(r[0], r[1], r[2], color = 'black')
        else: 
            self.ax.grid(True)
            self.ax.scatter(r[0], r[1], color = 'black')
    
    def click(self):
        self.back.clicked.connect(lambda: self.SetWidgetFalse())
        self.calcul.clicked.connect(lambda: self.CalculateExtr())
        
        self.cb_graph.stateChanged.connect(lambda: self.ChangeOutput())
    
    def ChangeOutput(self):
        if self.cb_graph.isChecked():
            self.cb_graph.setText('3д график')
        else:
            self.cb_graph.setText('Градиент')
    
    #sin(sqrt(x*x+y*y))


# #### СТАРТОВОЕ ОКНО

# In[17]:


#Общими усилиями

class StartWindow(Window):
    def __init__(self):
        Window.__init__(self, ui = 'start_line.ui')
        
        self.counter = 0
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(20)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(0)
        self.shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.dropShadowFrame.setGraphicsEffect(self.shadow)

        ## QTIMER ==> START
        self.timer = QTimer()
        self.timer.timeout.connect(self.progress)
        # TIMER IN MILLISECONDS
        self.timer.start(35)

        # CHANGE DESCRIPTION

        # Initial Text
        self.ui.label_description.setText("<strong>ДОБРО ПОЖАЛОВАТЬ</strong>")

        # Change Texts
        QTimer.singleShot(1500, lambda: self.ui.label_description.setText("<strong>LOADING</strong> DATABASE"))
        QTimer.singleShot(3000, lambda: self.ui.label_description.setText("<strong>LOADING</strong> USER INTERFACE"))


        ## SHOW ==> MAIN WINDOW
        ########################################################################
        self.show()
        ## ==> END ##

    ## ==> APP FUNCTIONS
    ########################################################################
    def progress(self):

        # SET VALUE TO PROGRESS BAR
        self.ui.progressBar.setValue(self.counter)

        # CLOSE SPLASH SCREE AND OPEN APP
        if self.counter > 100:
            # STOP TIMER
            self.timer.stop()

            # SHOW MAIN WINDOW
            self.main = MainWindow()
            self.main.show()

            # CLOSE SPLASH SCREEN
            self.close()

        # INCREASE COUNTER
        self.counter += 1


# In[18]:


def main():
    currentExitCode = Window.EXIT_CODE_REBOOT
    while currentExitCode == MainWindow.EXIT_CODE_REBOOT:
        app = QApplication(sys.argv)
        #window = MainWindow()
        #window = WindowGraph()
        window = StartWindow()
        window.show()
        currentExitCode = app.exec_()
        app = None


# In[ ]:


if __name__ == '__main__':
     main()


# In[ ]:


#https://pypi.org/project/numexpr/2.6.1/

