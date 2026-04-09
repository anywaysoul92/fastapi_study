# 요청 본문의 게이터 형식 관리
from pydantic import BaseModel, Field

# 사용자 추가할 때, 클라이언트가 서버로 보내는 데이터의 형식
    # id: int 중복이나 덮어쓰기 등의 문제로 시스템이 자동 생성하도록
    # 입력하지 않는다. 
class UserCreateRequest(BaseModel):
    name: str  = Field(..., min_length=2, max_length=10) # 2글자~10글자 (라이브러리 Field로)
    job: str  

# 클래스 -> 설계도, 요구조건 

#사용자 데이터를 수정할 때 데이터 형식 
class UserUpdateRequest(BaseModel):
    job: str


