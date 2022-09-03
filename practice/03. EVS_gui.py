from PyQt5.QtWidgets import *
import sys

class voting(QWidget):                                                      # 투표 탭
    def __init__(self):
        super().__init__()

        self.menu_group_box = QGroupBox('메뉴')
        self.fetch_vote_button = QPushButton('투표 조회')

        self.menu_hbox_layout = QHBoxLayout()
        self.menu_hbox_layout.addWidget(self.fetch_vote_button)

        self.menu_group_box.setLayout(self.menu_hbox_layout)                # 메뉴 그룹 박스

        #######################################################################################
        self.vote_list_group_box = QGroupBox('투표 목록')

        self.vote_list = QListWidget()
        self.vote_list.addItem('투표 1')
        self.vote_list.addItem('투표 2')

        self.vote_list_vbox_layout = QVBoxLayout()
        self.vote_list_vbox_layout.addWidget(self.vote_list)

        self.vote_group_vbox_layout.setLayout(self.vote_list_vbox_layout)   # 투표 목록 그룹 박스

###############################################################################################
        self.vote_info_group_box = QGroupBox()

        self.question_label = QLabel()
        self.question_label.setText('투표 질문')

        self.option1_button = QPushButton('선택지 1')
        self.option2_button = QPushButton('선택지 1')
        self.option3_button = QPushButton('선택지 1')

        self.vote_info_vbox_latyout = QVBoxLayout()
        self.vote_info_vbox_latyout.addWidget(self.question_label)
        self.vote_info_vbox_latyout.addWidget(self.option1_button)
        self.vote_info_vbox_latyout.addWidget(self.option2_button)
        self.vote_info_vbox_latyout.addWidget(self.option3_button)

        self.vote_layout = QGridLayout()                                     # 그룹 박스 -> 그리드
        self.vote_layout.addWidget(self.menu_hbox_layout, 0, 0, 1, 2)
        self.vote_layout.addWidget(self.vote_list_group_box, 1, 0, 1, 1)
        self.vote_layout.addWidget(self.vote_info_group_box, 1, 1, 1, 1)

###############################################################################################
        self.line_edit = QLineEdit()                                 # 입력 가능한 입력창 생성

        self.answer_button1 = QPushButton('A1')
        self.answer_button1.clicked.connect(self.selectButton_click)
        self.answer_button2 = QPushButton('A2')
        self.answer_button2.clicked.connect(self.selectButton_click)
        self.answer_button3 = QPushButton('A3')
        self.answer_button3.clicked.connect(self.selectButton_click)

        self.hbox_layout2 = QVBoxLayout()
        self.hbox_layout2.addWidget(self.answer_button1)
        self.hbox_layout2.addWidget(self.answer_button2)
        self.hbox_layout2.addWidget(self.answer_button3)

        self.vote_box.setLayout(self.hbox_layout2)                   # 투표 그룹 박스

        self.progressbar1 = QProgressBar()
        self.progressbar1.setRange(0, 100)                           # 0일 때, 100퍼센트
        self.progressbar2 = QProgressBar()
        self.progressbar2.setRange(0, 100)                           # 0일 때, 100퍼센트
        self.progressbar3 = QProgressBar()
        self.progressbar3.setRange(0, 100)                           # 0일 때, 100퍼센트

        self.value1 = 0
        self.value2 = 0
        self.value3 = 0
        self.progressbar1.setValue(self.value1)
        self.progressbar2.setValue(self.value2)
        self.progressbar3.setValue(self.value3)

        self.vbox_layout = QVBoxLayout()
        self.vbox_layout.addWidget(self.progressbar1)
        self.vbox_layout.addWidget(self.progressbar2)
        self.vbox_layout.addWidget(self.progressbar3)

        self.result_box.setLayout(self.vbox_layout)                  # 투표 결과 그룹 박스

    def selectButton_click(self):                                    # '+1' 버튼 클릭 시, 숫자 및 프로그레스 바 수치 증가
        self.value += 1
        self.progressbar.setValue(self.value)

###############################################################################################
class createVote(QWidget):                                           # 투표 생성 탭
    def __init__(self):
        super().__init__()

        self.form_layout = QFormLayout()
        self.question_line_edit = QLineEdit()
        self.option1_line_edit = QLineEdit()
        self.option2_line_edit = QLineEdit()
        self.option3_line_edit = QLineEdit()

        self.publish_button = QPushButton('생성')
        self.publish_button.clicked.connect(self.createButton)

        self.clear_button = QPushButton('초기화')
        self.clear_button.clicked.connect(self.resetButton)

        self.publish_clear_hbox_layout = QHBoxLayout()
        self.publish_clear_hbox_layout.addWidget(self.publish_button)
        self.publish_clear_hbox_layout.addWidget(self.clear_button)

        self.form_layout.addRow('질문 : ', self.question_line_edit)
        self.form_layout.addRow('선택지 : ', self.option1_line_edit)
        self.form_layout.addRow('', self.option2_line_edit)
        self.form_layout.addRow('', self.option3_line_edit)
        self.form_layout.addRow('', self.publish_clear_hbox_layout)

        self.setLayout(self.form_layout)

    def createButton(self):
        pass

    def resetButton(self):
        self.Question_line.setText('')
        self.Answer_line1.setText('')
        self.Answer_line2.setText('')
        self.Answer_line3.setText('')

###############################################################################################
class CentralizedElectronicVotingSystem(QWidget):                    # Main - 중앙 전자 투표 시스템
    def __init__(self):
        super().__init__()
        self.setWindowTitle('중앙 전자 투표 시스템')

        self.tab1 = voting()
        self.tab2 = createVote()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.tab1, '투표')
        self.tabs.addTab(self.tab2, '투표 생성')

        self.vbox_layout = QVBoxLayout()
        self.vbox_layout.addWidget(self.tabs)

        self.setLayout(self.vbox_layout)

def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    exit(1)                                                           # 예외 처리 (에러 발생하더라도 결과 확인)

if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    cevs = CentralizedElectronicVotingSystem()
    cevs.show()
    sys.exit(app.exec())