# server - 데이터를 받음 / 1:1 통신 / 중앙 서버가 없음 => 탈중앙화 구조
import socket

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   # (family(패밀리)= , type(소켓 타입/방식)= ) ipv4-고갈 가능성 있음, ipv6-사용성이 떨어짐
listen_socket.bind(('127.0.0.1', 6000))         # 컴퓨터 내부의 자기 자신의 로컬 네트워크 망 / 6000번 포트에 연결을 대기함 (비어 있는 포트면 상관 없음)
listen_socket.listen(1)                         # 위의 선언 다음 -> 실제로 대기하는 코드

connection, address = listen_socket.accept()    # connection, address로 받아오고 connection을 통해서 통신함
print('연결 됨:', address)

while True:
    message = connection.recv(1024)             # recv(receive) / 1024 - 통신할 바이트 단위 (=블록 단위 (=최대 바이트 수
    if len(message) == 0:                       # 연결이 끊어졌을 경우에만 빈 메세지를 받아옴
        print('연결 종료')
        listen_socket.close()
        break
    print('데이터 수신:', message)