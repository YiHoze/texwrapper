from math import factorial
from PyQt5.QtWidgets import  QWidget, QDesktopWidget, QLabel, QLineEdit, QPushButton, QPlainTextEdit, QGridLayout, QApplication

class factorial_GUI(QWidget):

    def __init__(self):        
        super().__init__()        
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Factorial')
        self.resize(500, 300)
        self.center() 
        
        inputLabel = QLabel('Enter an integer')
        self.inputEdit = QLineEdit()
        clearButton = QPushButton('Clear')
        self.result = QPlainTextEdit('0')
        self.result.setReadOnly(True)
        
        grid = QGridLayout()        
        grid.addWidget(inputLabel, 1, 0)
        grid.addWidget(self.inputEdit, 1, 1)
        grid.addWidget(clearButton, 2, 0)
        grid.addWidget(self.result, 2, 1)        
        self.setLayout(grid)
        
        self.inputEdit.returnPressed.connect(self.onChanged)
        clearButton.clicked.connect(self.clear)
        self.show()

    def onChanged(self):
        val = self.inputEdit.text()
        try:
            r = factorial(int(val))
            r = format(r, ',')        
            self.result.setPlainText(r)
        except:
            msg = '"%s" is not an integer' %(val)
            self.result.setPlainText(msg)

    def clear(self):
        self.inputEdit.clear()
        self.result.clear()
        
    def center(self):        
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())       

if __name__ == '__main__':
    
    app = QApplication([])
    fac = factorial_GUI()
    app.exec_()
