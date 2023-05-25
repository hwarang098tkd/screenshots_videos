from load import show_ui
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtGui import QDrag

if __name__ == '__main__':
    # Load the UI
    login = show_ui()
    login.show()
