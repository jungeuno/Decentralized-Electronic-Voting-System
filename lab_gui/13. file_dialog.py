from PyQt5.QtWidgets import *
import sys
# 파일
class GUI(QWidget):                                     # QWidget 상속 받음
    def __init__(self):
        super().__init__()
        self.setWindowTitle('제목')

        self.button = QPushButton('파일 열기')
        self.button.clicked.connect(self.button_click)

        self.text_label = QLabel()

        self.hbox_layout = QHBoxLayout()                                  # 가로로 나열
        self.hbox_layout.addWidget(self.button)
        self.hbox_layout.addWidget(self.text_label)

        self.setLayout(self.hbox_layout)

    def button_click(self):
        path, _ = QFileDialog.getOpenFileName(self, '파일을 선택하세요', './', 'All Files (*.*)')           # 새로운 창에 적힐 제목, 초기 위치, 파일 확장자
        if path == '':
            self.text_label.setText('취소')
        else:
            self.text_label.setText('파일 경로: ' + path)                   # 절대 경로 출력

def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    exit(1)                                             # 예외 처리 (에러 발생하더라도 결과 확인)

if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec())