from PyQt5.QtWidgets import *
import sys

class GUI(QWidget):                                     # QWidget 상속 받음
    def __init__(self):
        super().__init__()
        self.setWindowTitle('제목')

        self.group_box = QGroupBox('그룹')

        self.button1 = QPushButton('버튼 1')
        self.button2 = QPushButton('버튼 2')

        self.hbox_layout = QHBoxLayout()
        self.hbox_layout.addWidget(self.button1)        # 버튼들을 그룹지어줌
        self.hbox_layout.addWidget(self.button2)

        self.group_box.setLayout(self.hbox_layout)

        self.grid_layout = QGridLayout()
        self.grid_layout.addWidget(self.group_box, 0, 0, 1, 1)

        self.setLayout(self.grid_layout)

def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    exit(1)                                             # 예외 처리 (에러 발생하더라도 결과 확인)

if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec())