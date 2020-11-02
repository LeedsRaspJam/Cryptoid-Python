from PyQt5 import QtWidgets, uic
import sys

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        uic.loadUi('mainwindow.ui', self)

        self.doAThing.clicked.connect(self.buttonFunction)
        self.actionQuit.triggered.connect(self.closeApp)

    def buttonFunction(self):
        global textState
        try: 
            textState
        except NameError: 
            textState = "Default"

        if textState == "Default":
            self.mwLabel.setText("World Hello!")
            textState = "Changed"
        elif textState == "Changed":
            self.mwLabel.setText("Hello World!")
            textState = "Default"

    def closeApp(self):
        sys.exit()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':         
    main()