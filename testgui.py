from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel 
from PyQt5.QtCore import pyqtSignal, QThread
from file_reader import Patient
from time import sleep
import sys

class WorkerThread(QThread):
    finished = pyqtSignal(object)
    loopsignal = pyqtSignal(str)
    
    def __init__(self, function):
        super().__init__()
        self.function = function
        self.current_value = 0
        
    def run(self):
        while True:
            result = self.function()
            print(result)
            sleep(1)
            if self.current_value != result:
                self.finished.emit(result)
    

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.showMaximized()
        self.patient = Patient()
        self.functhread = 0
        self.write = False
        self.refresh = False
        self.runFunction1()

    def initUI(self):
        self.setWindowTitle('PyQt5 Button App')
        self.setGeometry(100, 100, 400, 200)

        self.value_display = QLabel(self)
        self.value_display.setText("bruh")
        self.value_display.setGeometry(260, 50, 300, 50)

        self.PI_Upper = QLabel(self)
        self.PI_Lower = QLabel(self)
        self.VF_Upper = QLabel(self)
        self.VF_Lower = QLabel(self)
#
        self.PI_Upper.setText("PIU")
        self.PI_Lower.setText("PIL")
        self.VF_Upper.setText("VFU")
        self.VF_Lower.setText("VFL")
        
        self.PI_Upper.setGeometry(700, 50, 300, 50)
        self.PI_Lower.setGeometry(700, 75, 300, 50)
        self.VF_Upper.setGeometry(750, 50, 300, 50)
        self.VF_Lower.setGeometry(750, 75, 300, 50)

        self.button1 = QPushButton('Confirm Value', self)
        self.button1.setGeometry(50, 100, 150, 50)
        self.button1.clicked.connect(self.function2)

        self.button2 = QPushButton('2', self)
        self.button2.setGeometry(200, 100, 150, 50)
        self.button2.clicked.connect(self.function2)

        self.button3 = QPushButton('Monophasic', self)
        self.button3.setGeometry(350, 100, 150, 50)
        self.button3.clicked.connect(self.function3)

    def runFunction1(self):
        #self.value_display.setText("Loading")
        self.functhread = WorkerThread(function=self.function1)
        self.functhread.finished.connect(self.displayResult)
        self.functhread.start()

    # def runFunction2(self):
    #     self.functhread = WorkerThread(function=self.function2)
    #     #self.functhread.finished.connect()
    #     self.functhread.start()
    #     #self.functhread.join()

    # def runFunction3(self):
    #     self.functhread = WorkerThread(function=self.function3)
    #     #self.functhread.finished.connect()
    #     self.functhread.start()

    def displayResult(self, result):
        self.value_display.setText(f'Result: {result}')

    def function1(self):
        print("hello")
        result = self.patient.value_hunter()
        return result
    
    def function2(self):
        self.patient.value_holder()
        self.vessel_setter()
        
    def function3(self):
        self.patient.monophasic_values()
        self.vessel_setter()
       #return 1

    def vessel_setter(self):
        #print(self.patient.vessel_storage)
        vals = self.patient.vessel_storage[1]
        self.PI_Upper.setText(str(vals[0]))
        self.PI_Lower.setText(str(vals[1]))
        self.VF_Upper.setText(str(vals[2]))
        self.VF_Lower.setText(str(vals[3]))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
