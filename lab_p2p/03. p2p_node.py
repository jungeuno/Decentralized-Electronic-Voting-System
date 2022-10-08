# node - 하나의 실행에서 데이터를 주고 받음 (=> server + client) / anaconda prompt 에서 실행
import socket
import threading
import json

nodes = []
port = 6000

def listen():                                       # 연결 요청 (데이터를 받는 곳) / 데이터를 받을 준비를 하는 함수
    while True:
        connection, address = listen_socket.accept()
        nodes.append((connection, address))
        print('연결 됨:', address)
        receive_thread = threading.Thread(target=receive, args=(connection, address))   # 스레드를 통해 데이터를 받을 준비
        receive_thread.daemon = True
        receive_thread.start()

def receive(connection, address):                   # 데이터를 받는 곳
    while True:
        try:
            message = connection.recv(1024)
        except:
            print(f'{address} 연결 종료')
            nodes.remove((connection, address))
            break
        if len(message) == 0:
            print(f'{address} 연결 종료')
            nodes.remove((connection, address))
            break
        print(f'{address} 데이터 수신: {message}')
        data = json.loads(message)
        if data['type'] == 'connect':
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', data['data']['port']))
            nodes.append((s, f'127.0.0.1:{data["data"]["port"]}'))
        elif data['type'] == 'chat':
            print(f'{address}의 메세지: {data["data"]["chat"]}')

if __name__ == '__main__':
    while True:
        try:
            listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            listen_socket.bind(('127.0.0.1', port))
            listen_socket.listen(1)
            print(f'{port}포트 연결 대기')
            break
        except:
            port += 1

    listen_thread = threading.Thread(target=listen)
    listen_thread.daemon = True
    listen_thread.start()

    for p in range(6000, 6010):         # 최대 10명의 인원이 동시에 연결 가능 하도록 / 네트워크에 참여할 수 있는 최대 인원
        if p == port:
            continue
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', p))
            s.sendall(json.dumps({
                'type': 'connect',
                'data': {
                    'port': port
                }
            }).encode())
            nodes.append((s, f'127.0.0.1:{p}'))
        except:
            continue

    while True:
        data = input('=> ')
        if data == 'q':
            for node in nodes:
                node[0].close()
            break
        for node in nodes.copy():                   # 원본 훼손 가능성 떄문에 복사본을 반복함
            try:
                node[0].sendall(json.dumps({        # 모든 데이터를 모든 참여자들에게 보냄
                    'type': 'chat',
                    'data': {
                        'chat': data
                    }
                }).encode())
            except:
                nodes.remove(node)                  # 연결이 끊긴(문제가 생긴) 노드는 제거함 => 연결 검사를 진행해주어야 함