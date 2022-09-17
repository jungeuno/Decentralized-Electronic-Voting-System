import requests
import json
from PyQt5.QtWidgets import *
import sys

class voting(QWidget):                                                 # 투표 탭
    def __init__(self):
        super().__init__()

        self.menu_group_box = QGroupBox('메뉴')
        self.fetch_vote_button = QPushButton('투표 조회')
        self.fetch_vote_button.clicked.connect(self.fetch_vote)

        self.menu_hbox_layout = QHBoxLayout()
        self.menu_hbox_layout.addWidget(self.fetch_vote_button)

        self.menu_group_box.setLayout(self.menu_hbox_layout)           # 메뉴 그룹 박스
       ########################################################################################
        self.vote_list_group_box = QGroupBox('투표 목록')

        self.vote_list_widget = QListWidget()
        self.vote_list_widget.clicked.connect(self.select_vote)
        self.vote_list = dict()

        self.vote_list_layout = QVBoxLayout()
        self.vote_list_layout.addWidget(self.vote_list_widget)
        self.vote_list_group_box.setLayout(self.vote_list_layout)      # 투표 목록 그룹 박스
       ########################################################################################
        self.vote_info_group_box = QGroupBox('투표 정보')

        self.question_label = QLabel()
        self.question_label.setText('투표 질문')

        self.option1_button = QPushButton('선택지 1')
        self.option2_button = QPushButton('선택지 2')
        self.option3_button = QPushButton('선택지 3')
        self.option1_button.clicked.connect(self.vote1)
        self.option2_button.clicked.connect(self.vote2)
        self.option3_button.clicked.connect(self.vote3)

        self.vote_info_vbox_layout = QVBoxLayout()
        self.vote_info_vbox_layout.addWidget(self.question_label)
        self.vote_info_vbox_layout.addWidget(self.option1_button)
        self.vote_info_vbox_layout.addWidget(self.option2_button)
        self.vote_info_vbox_layout.addWidget(self.option3_button)

        self.vote_info_group_box.setLayout(self.vote_info_vbox_layout)      # 투표 질문 및 선택지 그룹 박스
       ######################################################################################
        self.vote_result_group_box = QGroupBox('투표 결과')
        self.option1_progressbar = QProgressBar()
        self.option2_progressbar = QProgressBar()
        self.option3_progressbar = QProgressBar()
        self.vote_result_layout = QVBoxLayout()
        self.vote_result_layout.addWidget(self.option1_progressbar)
        self.vote_result_layout.addWidget(self.option2_progressbar)
        self.vote_result_layout.addWidget(self.option3_progressbar)
        self.vote_result_group_box.setLayout(self.vote_result_layout)       # 투표 결과 그룹 박스

        self.vote_layout = QGridLayout()                                    # 그룹 박스 -> 그리드
        self.vote_layout.addWidget(self.menu_group_box, 0, 0, 1, 2)
        self.vote_layout.addWidget(self.vote_list_group_box, 1, 0, 1, 1)
        self.vote_layout.addWidget(self.vote_info_group_box, 1, 1, 1, 1)
        self.vote_layout.addWidget(self.vote_result_group_box, 2, 0, 1, 2)

        self.setLayout(self.vote_layout)

    def fetch_vote(self):
        res = requests.get('http://127.0.0.1:5000/list')
        block_chain = json.loads(res.text)
        self.vote_list.clear()
        self.vote_list_widget.clear()

        for block in block_chain:
            if block['type'] == 'open':                                                 # 투표 생성해 준 것에 대한 데이터
                self.vote_list_widget.addItem(block['data']['id'])
                self.vote_list[block['data']['id']] = block['data']
                self.vote_list[block['data']['id']]['total_vote'] = 0
                self.vote_list[block['data']['id']]['vote_count'] = dict()
                for option in block['data']['options']:
                    self.vote_list[block['data']['id']]['vote_count'][option] = 0
            elif block['type'] == 'vote':                                               # 현재 투표한 곳에 +1, 투표 total에 +1
                self.vote_list[block['data']['id']]['total_vote'] += 1
                self.vote_list[block['data']['id']]['vote_count'][block['data']['vote']] += 1

    def select_vote(self):
        self.current_vote_id = self.vote_list_widget.currentItem().text()               # 최근 등록된 투표 항목
        self.update_vote()

    def update_vote(self):                                                              # 탈중앙화에서 사용 / 투표 현황 등,, 갱신해주는 함수
        self.question_label.setText(self.vote_list[self.current_vote_id]['question'])

        self.option1_button.setText(self.vote_list[self.current_vote_id]['options'][0])
        self.option2_button.setText(self.vote_list[self.current_vote_id]['options'][1])
        self.option3_button.setText(self.vote_list[self.current_vote_id]['options'][2])

        self.option1_progressbar.setRange(0, self.vote_list[self.current_vote_id]['total_vote'])
        option1_text = self.vote_list[self.current_vote_id]['options'][0]               # total_vote 의 수에 따른 비율을 프로그레스바로 나타냄
        self.option1_progressbar.setValue(self.vote_list[self.current_vote_id]['vote_count'][option1_text])

        self.option2_progressbar.setRange(0, self.vote_list[self.current_vote_id]['total_vote'])
        option2_text = self.vote_list[self.current_vote_id]['options'][1]
        self.option2_progressbar.setValue(self.vote_list[self.current_vote_id]['vote_count'][option2_text])

        self.option3_progressbar.setRange(0, self.vote_list[self.current_vote_id]['total_vote'])
        option3_text = self.vote_list[self.current_vote_id]['options'][2]
        self.option3_progressbar.setValue(self.vote_list[self.current_vote_id]['vote_count'][option3_text])

    def vote1(self):                                                                   # 해당 선택지 버튼의 data{ id, vote } 정보 가짐
        headers = {'Content-Type': 'application/json'}

        id = self.current_vote_id
        vote = self.vote_list[self.current_vote_id]['options'][0]

        data = {'id': id, 'vote': vote}

        res = requests.post(
            'http://127.0.0.1:5000/vote',
            data=json.dumps(data),
            headers=headers
        )
        print(res.text)
        self.fetch_vote()
        self.update_vote()

    def vote2(self):
        headers = {'Content-Type': 'application/json'}

        id = self.current_vote_id
        vote = self.vote_list[self.current_vote_id]['options'][1]

        data = {'id': id, 'vote': vote}

        res = requests.post(
            'http://127.0.0.1:5000/vote',
            data=json.dumps(data),
            headers=headers
        )
        print(res.text)
        self.fetch_vote()
        self.update_vote()

    def vote3(self):
        headers = {'Content-Type': 'application/json'}

        id = self.current_vote_id
        vote = self.vote_list[self.current_vote_id]['options'][2]

        data = {'id': id, 'vote': vote}

        res = requests.post(
            'http://127.0.0.1:5000/vote',
            data=json.dumps(data),
            headers=headers
        )
        print(res.text)
        self.fetch_vote()
        self.update_vote()

###############################################################################################
class createVote(QWidget):                                           # 투표 생성 탭
    def __init__(self):
        super().__init__()

        self.form_layout = QFormLayout()
        self.question_line_edit = QLineEdit()                        # 질문 라인
        self.option1_line_edit = QLineEdit()                         # 선택지 라인
        self.option2_line_edit = QLineEdit()
        self.option3_line_edit = QLineEdit()

        self.publish_button = QPushButton('생성')
        self.publish_button.clicked.connect(self.createButton)       # createButton() 함수 호출

        self.clear_button = QPushButton('초기화')
        self.clear_button.clicked.connect(self.resetButton)          # resetButton() 함수 호출

        self.publish_clear_hbox_layout = QHBoxLayout()
        self.publish_clear_hbox_layout.addWidget(self.publish_button)
        self.publish_clear_hbox_layout.addWidget(self.clear_button)

        self.form_layout.addRow('질문 : ', self.question_line_edit)
        self.form_layout.addRow('선택지 : ', self.option1_line_edit)
        self.form_layout.addRow('', self.option2_line_edit)
        self.form_layout.addRow('', self.option3_line_edit)
        self.form_layout.addRow('', self.publish_clear_hbox_layout)

        self.setLayout(self.form_layout)

    def createButton(self):                                          # 투표 생성 기능
        question = self.question_line_edit.text()
        option1 = self.option1_line_edit.text()
        option2 = self.option2_line_edit.text()
        option3 = self.option3_line_edit.text()

        headers = {'Content-Type': 'application/json'}

        data = {
            'question': question,                                    # 투표 질문
            'options': [option1, option2, option3]                   # 투표 선택지
        }

        res = requests.post(
            'http://127.0.0.1:5000/open',
            data=json.dumps(data),
            headers=headers
        )
        print(res.text)
        self.resetButton()

    def resetButton(self):                                            # 초기화 기능
        self.question_line_edit.setText('')
        self.option1_line_edit.setText('')
        self.option2_line_edit.setText('')
        self.option3_line_edit.setText('')

###############################################################################################
class CentralizedElectronicVotingSystem(QWidget):                    # Main - 중앙 전자 투표 시스템
    def __init__(self):
        super().__init__()
        self.setWindowTitle('중앙 전자 투표 시스템')

        self.voting_tab = voting()
        self.createVote_tab = createVote()

        self.tabs = QTabWidget()
        self.tabs.addTab(self.voting_tab, '투표')
        self.tabs.addTab(self.createVote_tab, '투표 생성')

        self.vbox_layout = QVBoxLayout()
        self.vbox_layout.addWidget(self.tabs)

        self.setLayout(self.vbox_layout)

def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    exit(1)                                                         # 예외 처리 (에러 발생하더라도 결과 확인)

if __name__ == '__main__':
    sys.excepthook = exception_hook
    app = QApplication(sys.argv)
    cevs = CentralizedElectronicVotingSystem()
    cevs.show()
    sys.exit(app.exec())