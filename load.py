import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidgetItem, QFileDialog, QListWidget, QAbstractItemView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('detect_UI.ui', self)
        self.ui.listWidget_videos.setAcceptDrops(True)
        self.ui.listWidget_videos.setDragDropMode(QAbstractItemView.InternalMove)
        self.ui.action_add_video.clicked.connect(self.add_video)

    def add_video(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Video File", "", "Video Files (*.mp4 *.avi *.dav)")
        if file_path:
            item = QListWidgetItem(file_path)
            self.ui.listWidget_videos.addItem(item)



def show_ui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
