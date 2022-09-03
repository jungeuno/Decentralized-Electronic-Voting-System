from PyQt5.QtWidgets import *
import sys

class GUI(QWidget):                                     # QWidget 상속 받음
    def __init__(self):
        super().__init__()
        self.setWindowTitle('제목')

        self.progressbar = QProgressBar()
        self.progressbar.setRange(0, 100)               # 0일 때, 100퍼센트

        self.value = 0
        self.progressbar.setValue(self.value)

        self.button = QPushButton('+1')
        self.button.clicked.connect(self.button_click)

        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.progressbar, 0, 0, 1, 1)
        self.grid_layout.addWidget(self.button, 1, 0, 1, 1)

        self.setLayout(self.grid_layout)

    def button_click(self):                             # '+1' 버튼 클릭하면 숫자 및 프로그레스바 수치 증가
        self.value += 1
        self.progressbar.setValue(self.value)

def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    exit(1)                                             # 예외 처리 (에러 발생하더라도 결과 확인)

if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec())