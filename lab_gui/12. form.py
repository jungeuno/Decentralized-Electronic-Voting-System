from PyQt5.QtWidgets import *
import sys
# 폼 형식(제출 기능 활용 가능)
class GUI(QWidget):                                     # QWidget 상속 받음
    def __init__(self):
        super().__init__()
        self.setWindowTitle('제목')

        self.form_layout = QFormLayout()

        self.line_edit = QLineEdit()
        self.button = QPushButton('버튼')

        self.form_layout.addRow('텍스트: ', self.line_edit)
        self.form_layout.addRow('', self.button)

        self.setLayout(self.form_layout)

def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    exit(1)                                             # 예외 처리 (에러 발생하더라도 결과 확인)

if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec())