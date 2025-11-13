# Ai TCP/IP 클라이언트 예제 (ai_client.py)

# 기능:
# 사용자가 입력한 요청(JSON)을 서버로 전송

import socket   # 네트워크 통신 모듈
import json     # JSON 직렬화/역직렬화용

# 1. 서버 기본 설정
HOST = '192.168.0.100' # 서버의 IP 주소 (localhost)
PORT = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("서버에 연결되었습니다. (종료하려면 'exit' 입력)\n")

while True:
    mode = input("분석 모드 (length / sentiment / keyword): ").strip()

    if mode.lower() == "exit":
        client_socket.sendall(mode.encode())
        break

    # 분석할 텍스트 입력
    text = input("분석할 문장 입력: ").strip()

    # 요청 JSON 구성
    request = {"mode": mode, "text": text}

    # JSON 직렬화 후 서버로 전송
    client_socket.sendall(json.dumps(request, ensure_ascii=False).encode())

    # 서버 응답 수신
    data = client_socket.recv(2048).decode()
    try:
        response = json.loads(data)
        print(f"\n 서버 응답: {json.dumps(response, ensure_ascii=False, indent=2)}\n")
    except json.JSONDecodeError:
        print(f" 서버 응답 오류: {data}")


# 4. 연결 종료

client_socket.close()
print("클라이언트 종료 완료")