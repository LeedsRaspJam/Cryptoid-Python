import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Cryptoid")
        
        mwLabel = QLabel("Hello World!")
        mwLabel.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(mwLabel)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()