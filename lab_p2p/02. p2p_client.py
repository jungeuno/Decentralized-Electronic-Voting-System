# client - 데이터를 보냄
import socket

send_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
send_socket.connect(('127.0.0.1', 6000))        # 6000번 포트에 실제로 연결을 시도함

while True:
    data = input('=> ')
    if data == 'q':
        send_socket.close()
        break
    send_socket.sendall(data.encode())