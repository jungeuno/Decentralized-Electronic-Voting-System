# 위조가 발생하면 해당 블록체인을 폐기하도록 함
import base64
import hashlib

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import os
import sys

import json
import socket
import uuid
from ecdsa import SigningKey, VerifyingKey                      # 전자서명에 필요함 암호화 알고리즘(비대칭키), 암호키/공개키 - 유효성 검사

def get_block_hash(block):
    data = dict()
    data['type'] = block['transaction']['type']
    data['data'] = sorted(block['transaction']['data'].copy().items())
    data['author'] = block['author']
    data['previous_hash'] = block['previous_hash']
    data = sorted(data.items())                                 # 딕셔너리 순서 보장이 안됨, 키 값을 기준으로 튜플 리스트 정렬을 통해 순서가 달라져도 같은 문자열이도록 함
    return hashlib.sha256(str(data).encode()).hexdigest()       # 문자열을 변환 후, 16진수로 변환(바이트 형태를 보기 편하도록, 복잡성 해소)

def get_block_signature(block, key):
    data = dict()
    data['type'] = block['transaction']['type']
    data['data'] = block['transaction']['data']
    data['autohr'] = block['author']
    data['previous_hash'] = block['previous_hash']
    data = sorted(data.items())
    signature = key.sign(str(data).encode())
    return base64.b64encode(signature).decode()                 # base64 - 바이트를 넣어도 알파벳으로 변환해주는 알고리즘, 보기 편하도록 알파벳으로 변환함

# 블록 해시
def verify_block_hash(block):
    block_hash = get_block_hash(block)
    if block_hash != block['hash']:
        return False
    return True

# 전자 서명
def verify_block_signature(block):
    key = VerifyingKey.from_pem(block['author'].encode())       # 공개키를 가져옴, 작성자 정보 가져옴
    data = dict()
    try:        # 인코딩한 데이터를 복원 시켜서 원본값을 넣어줌, 전자서명이 원본 데이터로 부터 해당 키로 생성된 것인지 판별/검증 -> 위조 검증
        key.verify(base64.b64encode(block['signature'].encode()),str(data).encode())
    except:
        return False
    return True

def verify_block_chain(chain):
    if (not verify_block_hash(chain[0])) or chain[0]['transaction']['type'] != 'genesis':
        # 첫 번째 블록이 변조되지 않아야 하고, 체인의 0번지 트랜잭션의 타입의 값이 테네시스가 아니라면, 잘못된 것/유효한 블록체인이 아니라는 것
        return False

        # 이전 블록의 해시값과 자신의 이력에 기록된 블록들의 해시값이 같은지 검사
    for i in range(1, len(chain)):
        if not verify_block_hash(chain[i]):
            return False
        if not verify_block_signature(chain[i]):
            return False
        if chain[i]['previous_hash'] != chain[i-1]['hash']:
            return False
    return True

##############################################################################################################
# 지갑/투표 UI 및 기능 구성
class Tab1(QWidget):
    def __init__(self, devs):
        super().__init__()

        self.devs = devs
        self.current_vote_id = -1

        self.wallet_group_box = QGroupBox('지갑')

        self.wallet_info_label = QLabel()
        self.wallet_info_label.setText('')

        # 지갑 생성 버튼
        self.wallet_generate_button = QPushButton('지갑 생성')
        self.wallet_generate_button.clicked.connect(self.generate_wallet)
        self.wallet_select_button = QPushButton('지각 선택')
        self.wallet_select_button.clicked.connect(self.select_wallet)
        self.wallet_layout = QHBoxLayout()
        self.wallet_layout.addWidget(self.wallet_info_label)
        self.wallet_layout.addWidget(self.wallet_generate_button)
        self.wallet_layout.addWidget(self.wallet_select_button)
        self.wallet_group_box.setLayout(self.wallet_layout)

        self.vote_list_group_box = QGroupBox('투표 목록')
        self.vote_list = dict()                                 # 실제 데이터를 담을 배열
        self.vote_list_widget = QListWidget()
        self.vote_list_widget.clicked.connect(self.select_vote)
        self.vote_list_layout = QVBoxLayout()
        self.vote_list_layout.addWidget(self.vote_list_widget)
        self.vote_list_group_box.setLayout(self.vote_list_layout)

        # 투표 생성 화면
        self.vote_group_box - QGroupBox('투표')
        self.question_label = QLabel()

        self.option1_button = QPushButton()
        self.option2_button = QPushButton()
        self.option3_button = QPushButton()

        self.option1_button.clicked.connect(self.vote1)
        self.option2_button.clicked.connect(self.vote2)
        self.option3_button.clicked.connect(self.vote3)

        self.vote_layout = QVBoxLayout()
        self.vote_layout.addWidget(self.question_label)
        self.vote_layout.addWidget(self.option1_button)
        self.vote_layout.addWidget(self.option2_button)
        self.vote_layout.addWidget(self.option3_button)
        self.vote_group_box.setLayout(self.vote_layout)

        # 투표 결과 화면
        self.vote_result_group_box = QGroupBox('투표 결과')
        self.option1_progressbar = QProgressBar()
        self.option2_progressbar = QProgressBar()
        self.option3_progressbar = QProgressBar()
        self.vote_result_layout = QVBoxLayout()
        self.vote_result_layout.addWidget(self.option1_progressbar)
        self.vote_result_layout.addWidget(self.option2_progressbar)
        self.vote_result_layout.addWidget(self.option3_progressbar)
        self.vote_result_group_box.setLayout(self.vote_result_layout)

        self.main_layout = QGridLayout()
        self.main_layout.addWidget(self.wallet_group_box, 0, 0, 1, 2)
        self.main_layout.addWidget(self.vote_list_group_box, 1, 0, 1, 1)
        self.main_layout.addWidget(self.vote_group_box, 1, 1, 1, 1)
        self.main_layout.addWidget(self.vote_result_group_box, 2, 0, 1, 2)

        self.update_wallet_info()                               # 지갑 정보 갱신 함수
        self.update_vote_list()

    # 지갑 생성
    def generate_wallet(self):
        self.devs.private_key = SigningKey.generate()
        self.devs.public_key = self.devs.private_key.get_verifying_key()
        self.devs.wallet_address = hashlib.sha256(self.devs.public_key.to_string()).hexdigest()

        if not os.path.exists('../wallets'):
            os.mkdir('../wallets')

        f = open(f'../wallets/{self.devs.wallet_address}.pem', 'wb')
        f.write(self.dwcs.private_key.to_pem())
        f.close()

        self.update_wallet_info()

    # 지갑 선택
    def select_wallet(self):
        path, _ = QFileDialog.getOpenFileName(self, '지갑 선택', '../wallets', 'PEM Files (*.pem)')
        if path == '':
            return

        f = open(path, 'rb')
        pem = f.read()
        f.close()

        self.dwvs.private_key = SigningKey.from_pem(pem)
        self.devs.public_key = self.devs.private_key.get_verifying_key()
        self.devs.wallet_address = hashlib.sha256(self.devs.public_key.to_string()).hexdigest()
        self.update_wallet_info()

    # 지갑 주소를 화면에 보여주는 기능
    def update_wallet_info(self):
        self.wallet_info_label.setText(f'지갑 주쇠: {self.devs.wallet_address}')

    # 투표 리스트를 화면에 보여주는 기능
    def update_vote_list(self):
        self.vote_list.clear()
        self.vote_list_widget.clear()
        for block in self.devs.chain:
            if block['transaction']['type'] == 'open':
                id = block['transaction']['data']['id']
                self.vote_list_widget.addItem(id)
                self.vote_list[id] = block['transaction']['data'].copy()
                self.vote_list[id]['total_vote'] = 0
                self.vote_list[id]['vote_count'] = dict()
                for option in block['transaction']['data']['options']:
                    self.vote_list[id]['vote_count'][option] = 0
            elif block['transaction']['type'] == 'vote':
                id = block['transaction']['data']['id']
                self.vote_list[id]['total_vote'] += 1
                self.vote_list[id]['vote_count'][block['transaction']['data']['vote']] += 1
        self.update_vote()

    # 투표 선택
    def select_vote(self):
        self.current_vote_id = self.vote_list_widget.currentItem().text()
        self.update_vote()

    # 투표 갱신/업데이트
    def update_vote(self):
        if self.current_vote_id not in self.vote_list:
            return

        self.question_label.setText(self.vote_list[self.current_vote_id]['question'])

        option1 = self.vote_list[self.current_vote_id]['options'][0]
        self.option1_button.setText(option1)
        self.option1_progressbar.setRange(0, self.vote_list[self.current_vote_id]['total_vote'])
        self.option1_progressbar.setValue(self.vote_list[self.current_vote_id]['vote_count'][option1])

        option2 = self.vote_list[self.current_vote_id]['options'][1]
        self.option2_button.setText(option2)
        self.option2_progressbar.setRange(0, self.vote_list[self.current_vote_id]['total_vote'])
        self.option2_progressbar.setValue(self.vote_list[self.current_vote_id]['vote_count'][option2])

        option3 = self.vote_list[self.current_vote_id]['options'][2]
        self.option3_button.setText(option3)
        self.option3_progressbar.setRange(0, self.vote_list[self.current_vote_id]['total_vote'])
        self.option3_progressbar.setValue(self.vote_list[self.current_vote_id]['vote_count'][option3])

    def vote1(self):
        block = {
            'transaction': {
                'type': 'vote',
                'data': {
                    'id': self.current_vote_id,
                    'vote': self.option1_button.text()
                }
            },
            'author': self. devs.public_key.to_pem().decode(),                              # 작성자가 추가됨
            'previous_hash': self.devs.chain[-1]['hash']
        }
        block['hash'] = get_block_hash(block)
        block['signature'] = get_block_signature(block, self.devs.private_key)              # 위조가 방지된 블록체인
        self.devs.chain.append(block)
        for node in self.devs.nodes.copy():
            try:
                node[0].sendall(json.dumps(block).encode())
            except:
                self.devs.nodes.remove(node)
        self.update_vote_list()

    def vote2(self):
        block = {
            'transaction': {
                'type': 'vote',
                'data': {
                    'id': self.current_vote_id,
                    'vote': self.option2_button.text()
                }
            },
            'author': self.devs.public_key.to_pem().decode(),
            'previous_hash': self.devs.chain[-1]['hash']
        }
        block['hash'] = get_block_hash(block)
        block['signature'] = get_block_signature(block, self.devs.private_key)
        self.devs.chain.append(block)
        for node in self.nodes.copy():
            try:
                node[0].sendall(json.dumps(block).encode())
            except:
                self.devs.nodes.remove(node)
        self.update_vote_list()

    def vote3(self):
        block = {
            'transaction': {
                'type': 'vote',
                'data': {
                    'id': self.current_vote_id,
                    'vote': self.option3_button.text()
                }
            },
            'author': self.devs.public_key.to_pem().decode(),
            'previous_hash': self.devs.chain[-1]['hash']
        }
        block['hash'] = get_block_hash(block)
        block['signature'] = get_block_signature(block, self.devs.private_key)
        self.devs.chain.append(block)
        for node in self.nodes.copy():
            try:
                node[0].sendall(json.dumps(block).encode())
            except:
                self.devs.nodes.remove(node)
        self.update_vote_list()

##############################################################################################################
# 투표 생성 UI 및 기능 구성
class Tab2(QWidget):
    def __init__(self,devs):
        super().__init__()

        self.devs = devs

        self.form_layout = QFormLayout()

        self.question_line_edit = QLineEdit()

        self.option1_line_edit = QLineEdit()
        self.option2_line_edit = QLineEdit()
        self.option3_line_edit = QLineEdit()

        self.publish_clear_layout = QHBoxLayout()

        self.publish_button = QPushButton('게시')
        self.publish_button.clicked.connect(self.publish_form)

        self.clear_button = QPushButton('초기화')
        self.clear_button.clicked.connect(self.clear_form)
        self.publish_clear_layout.addWidget(self.publish_button)
        self.publish_clear_layout.addWidget(self.clear_button)

        self.form_layout.addRow('질문: ', self.question_line_edit)
        self.form_layout.addRow('선택지: ', self.option1_line_edit)
        self.form_layout.addRow('', self.option2_line_edit)
        self.form_layout.addRow('', self.option3_line_edit)
        self.form_layout.addRow('', self.publish_clear_layout)

        self.setLayout(self.form_layout)

    # '게시' 버튼 기능 구현
    def publish_form(self):
        block = {
            'transaction' : {
                'type': 'open',
                'data': {
                    'id': str(uuid.uuid4()),
                    'question': self.question_line_edit.text(),
                    'options': [
                        self.option1_line_edit.text,
                        self.option2_line_edit.text,
                        self.option3_line_edit.text
                    ]
                }
            },
            'author': self.devs.public_key.to_pem().decode(),
            'previous_hash': self.devs.chain[-1]['hash']
        }
        block['hash'] = get_block_hash(block)
        block['signature'] = get_block_signature(block, self.devs.private_key)
        self.devs.chain.append(block)
        for node in self.devs.node.copy():
            try:
                node[0].sendall(json.dumps(block).encode())
            except:
                self.devs.nodes.remove(node)
        self.devs.tab1.update_vote_list()

    # form 초기화
    def clear_form(self):
        self.question_line_edit.setText('')
        self.option1_line_edit.setText('')
        self.option2_line_edit.setText('')
        self.option3_line_edit.setText('')

##############################################################################################################
# 변조와 위조 가능한 클래스, [해킹]
class Tab3(QWidget):
    def __init__(self, devs):
        super().__init__()

        self.devs = devs

        modify_button = QPushButton("변조")
        modify_button.clicked.connect(self.modify)

        forgery_button = QPushButton("위조")
        forgery_button.clicked.connect(self.forgery)

        layout = QVBoxLayout()
        layout.addWidget(modify_button)
        layout.addWidget(forgery_button)
        layout.addStretch(1)

        self.setLayout(layout)

    def modify(self):
        self.devs.chain[-1]['transaction']['type'] = 'open'
        self.devs.chain[-1]['transaction']['data']['id'] = 'hack'
        self.devs.chain[-1]['transaction']['data']['question'] = 'hack'
        self.devs.chain[-1]['transaction']['data']['options'] = ['hack1', 'hack2', 'hack3']
        self.devs.vote_list_tab.update_vote_list()

    def forgery(self):
        block = {
            'transaction': {
                'type': 'open',
                'data': {
                    'id': 'hack',
                    'question': 'hack',
                    'options': ['hack1', 'hack2', 'hack3']
                }
            }
        }
        block['hash'] = get_block_hash(block)
        self.devs.chain.append(block)

        block = {
            'transaction': {
                'type': 'vote',
                'data': {
                    'id': 'hack',
                    'vote': 'hack3',
                }
            }
        }
        block['hash'] = get_block_hash(block)
        self.devs.chain.append(block)
        self.devs.vote_list_tab.update_vote_list()

##############################################################################################################
# 소켓 통신
class SocketReceiver(QThread):
    update_vote_list_signal = pyqtSignal()

    def __init__(self, devs, connection, address):
        super().__init__()
        self.devs = devs
        self.connection = connection
        self.address = address

    def run(self):
        while True:
            try:
                message = self.connection.recv(10240)
            except:
                print(f'{self.address} 연결 종료')
                break
            if len(message) == 0:
                print(f'{self.address} 연결 종료')
                break
            print(f"{self.address} 데이터 수신: {message}")
            data = json.loads(message)
            if data['transaction']['type'] == 'connect':
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('127.0.0.1', data['transaction']['data']['port']))
                block = {
                    'transaction': {
                        'type': 'list',
                        'data': {
                            'chain': self.devs.chain
                        }
                    }
                }
                s.sendall(json.dumps(block).encode())
                self.devs.nodes.append((s, f'127.0.0.1:{data["transaction"]["data"]["port"]}'))
            elif data['transaction']['type'] == 'list':
                if verify_block_chain(data['transaction']['data']['chain']):
                    self.devs.chain = data['transaction']['data']['chain']
                    self.update_vote_list_signal.emit()
                else:
                    print('블록체인 위변조 감지')
            elif data['transaction']['type'] == 'open':
                if verify_block_signature(data):
                    self.devs.chain.append(data)
                    self.update_vote_list_signal.emit()
                else:
                    print('블록 위변조 감지')
            elif data['transaction']['type'] == 'vote':
                if verify_block_signature(data):
                    self.devs.chain.append(data)
                    self.update_vote_list_signal.emit()
                else:
                    print('블록 위변조 감지')


class SocketListener(QThread):
    update_vote_list_signal = pyqtSignal()

    def __init__(self, devs):
        super().__init__()
        self.devs = devs

    def run(self):
        while True:
            connection, address = self.devs.listen_socket.accept()
            self.devs.nodes.append((connection, address))
            print("연결 됨: ", address)
            self.receive_thread = SocketReceiver(self.devs, connection, address)
            self.receive_thread.update_vote_list_signal.connect(self.update_vote_list)
            self.receive_thread.start()

    @pyqtSlot()
    def update_vote_list(self):
        self.update_vote_list_signal.emit()


class SocketManager(QThread):
    update_vote_list_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.port = 6000

    def run(self):
        while True:
            try:
                self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.listen_socket.bind(('127.0.0.1', self.port))
                self.listen_socket.listen(1)
                print(f'{self.port}포트 연결 대기')
                break
            except:
                self.port += 1

        self.listen_thread = SocketListener(self)
        self.listen_thread.update_vote_list_signal.connect(self.update_vote_list)
        self.listen_thread.start()

        for p in range(6000, 6100):
            if p == self.port:
                continue
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('127.0.0.1', p))
                block = {
                    'transaction': {
                        'type': 'connect',
                        'data': {
                            'port': self.port
                        }
                    }
                }
                s.sendall(json.dumps(block).encode())
                self.nodes.append((s, f'127.0.0.1:{p}'))
            except:
                pass

    @pyqtSlot()
    def update_vote_list(self):
        self.update_vote_list_signal.emit()


class DecentralizedElectronicVotingSystem(QWidget):
    def __init__(self):
        super().__init__()

        genesis_block = {
            'transaction': {
                'type': 'genesis',
                'data': dict(),
            },
            'author': 'genesis',
            'previous_hash': None
        }
        genesis_block['hash'] = get_block_hash(genesis_block)

        self.chain = [genesis_block]
        self.nodes = []

        self.private_key = None
        self.public_key = None
        self.wallet_address = None

        self.setWindowTitle("탈중앙 블록체인 투표 시스템")

        self.vote_list_tab = Tab1(self)
        self.vote_tab = Tab2(self)
        self.hack_tab = Tab3(self)

        tabs = QTabWidget()
        tabs.addTab(self.vote_list_tab, '투표')
        tabs.addTab(self.vote_tab, '투표 생성')
        tabs.addTab(self.hack_tab, 'Hack')

        vbox = QVBoxLayout()
        vbox.addWidget(tabs)

        self.setLayout(vbox)

        port = 6000
        while True:
            try:
                self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.listen_socket.bind(('127.0.0.1', port))
                self.listen_socket.listen(1)
                print(f'{port}포트 연결 대기')
                break
            except:
                port += 1

        self.listen_thread = SocketListener(self)
        self.listen_thread.update_vote_list_signal.connect(self.update_vote_list)
        self.listen_thread.start()

        for p in range(6000, 6005):
            if p == port:
                continue
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect(('127.0.0.1', p))
                block = {
                    'transaction': {
                        'type': 'connect',
                        'data': {
                            'port': port
                        }
                    }
                }
                s.sendall(json.dumps(block).encode())
                self.nodes.append((s, f'127.0.0.1:{p}'))
            except:
                pass

    @pyqtSlot()
    def update_vote_list(self):
        self.vote_list_tab.update_vote_list()


def exception_hook(except_type, value, traceback):
    print(except_type, value, traceback)
    traceback.print_exc()
    exit(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys.excepthook = exception_hook
    devs = DecentralizedElectronicVotingSystem()
    devs.show()
    sys.exit(app.exec_())
