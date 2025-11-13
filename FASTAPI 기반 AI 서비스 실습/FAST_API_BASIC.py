# FASTAPI 기본 실습 예제

# 기능:
# GET 요청 => 서버 상태 확인
# POST 요청 -> 사용자 데이터를 받아 처리 후 응답

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI(
    title="FastAPI 기본 예제",
    description="PyCharm에서 실습 가능한 FastAPI 기본 예제",
    version="1.0.0"
)



# 2. 데이터 모델 정의 (POST 요청 시)
class Item(BaseModel):
    name: str                           # 필수: 아이템 이름
    price: float                        # 필수: 가격
    description: Optional[str] = None    # 선택: 설명

# 3. 기본 엔트포인트

@app.get("/")
def read_root():
    """
    서버 상태 확인용 기본 엔드포인트
    브라우저나 curl로 GET 요청 시 메시지 반환
    """
    return {"message": "FastAPI 서버가 정상적으로 동작 중입니다!"}

# 4. 단순한 GET 요청 예제

@app.get("/hello")
def say_hello(name: str = "사용자"):
    """
    GET 요청 시 URL 파라미터로 이름을 받아 인사 메시지를 반환
    """
    return {"message": f"안녕하세요 {name}님!"}

# 5. 단순한 POST 요청 예제

@app.post("/items")
def create_item(item: Item):

    total_price = item.price * 1.1
    return {
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "total_with_tax": total_price,
        "message": f"{item.name} 아이템이 성공적으로 등록되었습니다."
    }

# 6. FASTAPI 실행 (uvicorn)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="192.168.0.100", port=8000)