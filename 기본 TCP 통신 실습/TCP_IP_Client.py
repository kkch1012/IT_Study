# TCP/IP 클라이언트 예제

# 사용자가 입력한 메시지를 서버로 전송하고,
# 서버의 응답을 받아 출력하는 클라이언트입니다.

import socket # 네트워크 통신 모듈

# 1. 서버 기본 설정
HOST = '192.168.0.100' # 서버의 IP 주소 (localhost)
PORT = 9999


# 2. 소켓 생성

# IPv$(AF_INET) + TCP(socket_STREAM) 사용
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 3. 서버에 연결 시도
client_socket.connect((HOST, PORT))
print(f"서버({HOST}:{PORT})에 연결되었습니다.")
print("메시지를 입력하세요. (종료하려면 'exit' 입력)\n")


while True:
    # 사용자 입력 대기
    message = input("보낼 메시지: ")


    # 'exit' 입력 시 종료

    if message.lower() == 'exit':
        client_socket.sendall(message.encode())
        break

    # 서버로 메시지 전송
    client_socket.sendall(message.encode())

    # 서버로부터 응답 수신
    data = client_socket.recv(1024).decode()
    print(f"서버 응답: {data}\n")

client_socket.close()
print("클라이언트 종료 완료")