# AI TCP/IP 클라이언트 예제

import socket   # 네트워크 통신 모듈
import json     # JSON 직렬화/역직렬화용

# 1. 서버 기본 설정
HOST = '192.168.0.100' # 서버의 IP 주소 (localhost)
PORT = 9999

# 2. 분석 함수 정의

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

# TCP 서버 생성 및 설정
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()
print(f" AI 서버 실행 중...({HOST}:{PORT})")


#4 . 클라이언트 연결 수락

client_socket, addr = server_socket.accept()
print(f" 클라이언트 연결됨: {addr}")

#5. 클라이언트와 메시지 수신/응답 루프

while True:
    data = client_socket.recv(1024).decode()
    if not data:
        print(" 클라이언트 연결 종료 감지")
        break
    if data.lower() == "exit":
        print(" 클라이언트 종료 요청 감지")
        break

    try:
        request = json.loads(data)
        # 요청 분석 수행
        result = analyze_text(request)
    except json.JSONDecodeError:
        result = {"error": "잘못된 JSON 형식입니다."}

    # 응답을 JSON 문자열로 변환 후 인코딩
    response = json.dumps(result, ensure_ascii=False)
    client_socket.sendall(response.encode())
