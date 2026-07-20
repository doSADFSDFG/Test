from fastapi.testclient import TestClient
from app import app

# 가상 HTTP 요청을 날려줄 클라이언트 복제 가동
client = TestClient(app)

# ── [검증 1] 루트 경로가 정상(200)이고 hello를 뱉는지 검사 ──
def test_read_root_200():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "hello"}

# ── [검증 2] 아이템 조회가 정상(200) 작동하는지 검사 ──
def test_read_item_success():
    response = client.get("/items/42")
    assert response.status_code == 200
    assert response.json()["item_id"] == 42

# ── [검증 3] 주소에 숫자가 아닌 문자가 들어왔을 때 유효성 검사 ──
def test_read_item_validation_error():
    # item_id는 정수(int)여야 하는데 'abc'라는 문자열을 억지로 찔러봅니다.
    response = client.get("/items/abc")
    
    # FastAPI가 알아서 주입 차단(422 Unprocessable Entity 에러)을 해주는지 검증합니다.
    assert response.status_code == 422