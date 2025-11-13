# 멀티 클라이언트 지원 AI TCP 서버


# 기능:
# 여러 클라이언트가 동시에 접속 가능(thread 기반)
# 각 클라이언트가 Json 형태의 분석 요청을 보내면
# 서버는 분석 결과(JSON)를 응답함

import socket
import threading # 클라이언트별 쓰레드 처리용
import json     # JSON 데이터 직렬화/역직렬화용

# 1. 서버 기본 설정
HOST = '192.168.0.100' # 서버의 IP 주소 (localhost)
PORT = 9999         # 서버 포트 번호
MAX_CLIENTS = 5 # 동시에 연결 가능한 최대 클라이언트 수


def analyze_text(request):
    """
    클라이언트의 요청(JSON)을 받아 분석 결과를 반환하는 함수
    request: dict (예: {"mode": "sentiment", "text": "문장"})
    """
    mode = request.get('mode')
    text = request.get('text')

    #(1) 문자열 길이 분석
    if mode == "length":
        return {
            "result":len(text),
            "dec":f"문자 길이는 {len(text)}자 입니다."
        }
    #(2) 감성 분석(규칙기반)
    elif mode == "sentiment":
        if any(word in text for word in ["좋아", "행복", "멋져", "훌룡"]):
            sentiment = "positive"
        elif any(word in text for word in ["싫어", "불만", "짜증", "나빠"]):
            sentiment = "negative"
        else:
            sentiment = "neutral"
        return {
            "result":sentiment,
            "desc": f"감정 분석 결과: {sentiment}"
        }

    #(3) 키워드 탐지
    elif mode == "keyword":
        keywords = ["AI", "서비스", "생산", "불량", "데이터"]
        found = [k for k in keywords if k in text]
        return {
            "result":found,
            "desc": f"키워드 발견: {', '.join(found) if found else '없음'}"
        }
    #(4) 지원하지 않는 모드 처리
    else:
        return {"error": f"지원하지 않는 분석 모드입니다.: {mode}"}


# 3. 클라이언트 처리 스레드 함수

def handle_client(client_socket, address):

    print(f" 클라이언트 {address} 연결됨")

    while True:
        try:
            data =  client_socket.recv(2048).decode()

            if not data:
                print(f" {address} 연결 끊김")
                break

            if data.lower() == "exit":
                print(f" {address} 종료 요청 수신")
                break

            try:
                request = json.loads(data)
                result = analyze_text(request)
            except json.JSONDecodeError:
                result = {"error": "잘못된 JSON 형식입니다."}

            # 응답 전송
            response = json.dumps(result,ensure_ascii=False)
            client_socket.sendall(response.encode())

        except ConnectionResetError:
            print(f" {address} 비정상 종료")
            break

    client_socket.close()
    print(f"클라이언트 {address} 세션 종료 완료")


    # 4. 서버 메인 실행부

    def start_server():
        """
            메인 서버 함수: 클라이언트 접속을 대기하고,
            접속 시마다 새로운 스레드를 생성하여 handle_client 실행
            """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(MAX_CLIENTS)

        print(f"AI 서버 실행 중... {HOST}:{PORT}")
        print(f"최대 {MAX_CLIENTS}개의 클라이언트 동시 접속 가능\n")

        try:
            while True:
                # 클라이언트 연결 대기 (blocking)
                client_socket, addr = server_socket.accept()

                # 스레드 생성 및 실행
                client_thread = threading.Thread(
                    target=handle_client, args=(client_socket, addr), daemon=True
                )
                client_thread.start()

        except KeyboardInterrupt:
            print("\n 서버 수동 종료 감지")
        finally:
            server_socket.close()
            print("서버 완전 종료")
    # 5. 실행 시작
    if __name__ == "__main__":
        start_server()