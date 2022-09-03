from PyQt5.QtWidgets import *
import sys

class GUI(QWidget):                                     # QWidget 상속 받음
    def __init__(self):
        super().__init__()
        self.setWindowTitle('제목')

        self.line_edit = QLineEdit()                    # 입력 가능한 입력창 생성

        self.button = QPushButton('버튼')
        self.button.clicked.connect(self.button_click)

        self.text_label = QLabel()                      # 버튼 클릭하면 입력한 텍스트 출력되는 레이블 생성

        self.vbox_layout = QVBoxLayout()
        self.vbox_layout.addWidget(self.line_edit)
        self.vbox_layout.addWidget(self.button)
        self.vbox_layout.addWidget(self.text_label)

        self.setLayout(self.vbox_layout)

    def button_click(self):                             # 버튼 클릭 시, 텍스트 출력
        self.text_label.setText(self.line_edit.text())

def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    exit(1)                                             # 예외 처리 (에러 발생하더라도 결과 확인)

if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec())