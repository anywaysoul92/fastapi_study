from fastapi import APIRouter, Path, Query, status, HTTPException, Depends
from sqlalchemy import select, delete
from database.connection import SessionFactory
from user.models import User
from user.request import UserCreateRequest, UserUpdateRequest
from user.response import UserResponse
from database.connection import get_session


# 아래의 user 핸들러 함수들을 관리하는 객체
# router = APIRouter(prefix="/users")
router = APIRouter(tags=["User"])



# # 임시 데이터베이스 <- 이제 db 따로 있어서 필요없어짐 
# users = [
#         {"id": 1, "name": "alex", "job": "student"},
#         {"id": 2, "name": "bob", "job": "sw engineer"},
#         {"id": 3, "name": "chris", "job": "barista"},
#     ]

# 전체 사용자 목록 조회 API
# GET / users
@router.get(
        "/users",
        status_code=status.HTTP_200_OK,
        summary="전체 사용자 목록 조회 API",
        response_model=list[UserResponse], # type hint로 준다 
        )
def get_users_handler(
    # Depends: FastAPI에서 의존성(get_session)을 자동으로 실행/ 주입/ 정리 
    session = Depends(get_session), #  with SessionFactory() as session: 의존성 주입으로 삭제한 코드  
):
    #with SessionFactory() as session:
        # SELECT *FROM user;
        #statement = 구문(명령문)
    stmt = select(User) # SELECT * FROM user;
    result = session.execute(stmt)
    users = result.scalars().all() # [user1, user2, user3]
    return users

# 사용자 정보 검색 API
# GET /users/search?name=alex
# GET /users/search?job=student
# | None = Query(None) -> optional하게 하나만 있어도 오류 안나게 함  ,
@router.get(
        "/users/search",
        summary= "사용자 정보 검색 API",
        response_model=list[UserResponse]
        )
def search_user_handler(
    name: str | None = Query(None), 
    job: str | None = Query(None),
    session = Depends(get_session),
):
    stmt = select(User) # 체이닝
    if name:
        stmt = stmt.where(User.name == name)
        # stmt = select(User).where(User.name == name)
    if job: # elif 쓰면 job은 필터가 안되는 거니까 if, 동사 존재 가능
        stmt = stmt.where(User.job == job)
        # stmt = select(User).where(User.job == job, 

    # with SessionFactory() as session:
    result = session.execute(stmt)
    users = result.scalars().all()
    return users
    # stmt = select(User).where(User.job == job, User.name == name)
    # # 조건 둘다 검색할 수 있는

    # 둘 다 없을 때
    # if name is None and job is None:
    #     return {"msg": "조회에 필요한 QueryParam이 필요합니다."}
    # return {"name": name, "job": job}
# 둘 다 보낼 때
    # for user in users:
    #     if name and job:
    #         if user["name"] == name and user["job"] == job:
    #             return user
    #         else:
    #             return None
    #     if user["name"] == name:
    #         return user
    #     if user["job"] == job:
    #         return user

    
    
# 단일 사용자 데이터 조회 API
# GET /users/1 -> 1번 사용자 데이터 조회 등등
# 사용자가 만을 때는 변수로 받을 수 있게 한다.
# GET /users/{user_id} -> {user_id} 사용자 데이터 조회 등등
@router.get(
        "/users/{user_id}",
        summary="단일 사용자 데이터 조회 API",
        response_model=UserResponse
        )
def get_user_one_handler(
    #user_id: int  # : int -> 숫자로 바꾸는 문법
    #이상 (=Greater than or equal to, le=9999 less than, max_digits= 최대 몇자리 허용? ),
    #  '...' 의 의미는 필수 조건이라는 의미, Path(..., ge=1, le=9999, max_digits=)
    user_id: int = Path(..., ge=1),
    session = Depends(get_session),
):
    # with SessionFactory() as session:
    stmt = select(User).where(User.id == user_id) 
    # sql where 절, ID 맞는 애들 갖고 오는거라 1,0임
    # SELECT * FROM user WHERE id = 1; (예시)
    result = session.execute(stmt)

    # scalars() -> 첫번째 열의 데이터만 가져온다
    # all() -> 리스트로 변환한다
    
    #scalar 존재하면 user객체 반환 존재하지 않으면 None
    user = result.scalar()

    if not user:
        raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="User Not Found",
)
    return user 
    

    # for user in users:
    #     if user["id"] == user_id:
    #         return user
    #     # 없는 번호가 입력되면 None 반환 & 404 에러 반환
    
        

# 회원 추가 API
# POST /users
@router.post(
    "/users", 
    status_code=status.HTTP_201_CREATED,
    summary="회원 추가 API",
    response_model=UserResponse
)
def create_user_handler(
    # 1) 사용자 데이터를 넘겨 받는다 + 유효성 검사
    body: UserCreateRequest,
    session = Depends(get_session)
):
    
    # 2) 사용자 데이터를 저장한다
    # session = SessionFactory()

    # with SessionFactory() as session:
    new_user = User(name=body.name, job=body.job)

    session.add(new_user) # 새로운 유저 추가해라
    session.commit() # 변경사항 저장 
    session.refresh(new_user) #새로고침 (id, created_at 불러옴)
    return new_user
    


    # # 2) 사용자 데이터를 저장한다.
    # new_user = {
    #     "id": len(users) + 1, 
    #     "name": body.name,
    #     "job": body.job,
    # }
    # users.append(new_user)

    # # 3) 응답을 반환한다
    # return new_user
    

# 회원 정보 수정 API
#  PATCH /users/{users_id}
@router.patch(
        "/users/{user_id}",
        summary="회원 정보 수정 API",
        response_model=UserResponse,
        )
def update_user_handler(
    # 1) 입력값 정의: 클라이언트로부터 수정할 데이터를 넘겨 받는다 
    user_id: int,
    body: UserUpdateRequest,
    session = Depends(get_session)
):

    
    # 2) 처리
    # user_id로 사용자를 조회 
    # with SessionFactory() as session:
    stmt = select(User).where(User.id == user_id)
    result = session.execute(stmt)
    user = result.scalar()
    
    if not user:
    # 예외처리 먼저, 사용자가 없으면 none 반환 할 수 있어서 
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User Not Found",
)
    user.job = body.job
    # session.add() 필요없는이유: 처음부터 session에서 user를 가져와서 누군지 알아서
    # 굳이 add해서 stage에 올릴 필요가 없음 
    session.commit() # user 상태(job)을 DB에 반영한다
    # e.g. UPDATE user SET job = '  ' WHERE user.id = 1;
    return user # session을 닫는다 

    # for user in users:
    #     if user["id"] == user_id:
    #         # 데이터 수정
    #         user["job"] = body.job
    #         return user # 반환
    

# 회원 삭제 API
# DELETE /users/{user_id}
@router.delete(
        "/users/{user_id}",
        summary="회원 삭제 API",
        status_code=status.HTTP_204_NO_CONTENT, # 응답 본문이 비어있음 
        )
def delete_user_handler(
    user_id: int,
    session = Depends(get_session),
):
    # 1) get + delete
    #   user 정보 갖고와서 삭제
    # with SessionFactory() as session:
    #     stmt = select(User).where(User.id == user_id)
    #     result = session.execute(stmt)
    #     user = result.scalar()

    #     if not user:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND,
    #             detail="User Not Found",
    #     )

    #     session.delete(user) # 객체를 삭제 
    #     # session.expunge(user) -> session 추적대상에서 제거
    #     session.commit() 
    
    #조회없이 곧바로 삭제
    # with SessionFactory() as session:
    stmt = delete(User).where(User.id == user_id)
    session.execute(stmt)
    session.commit()



    # 2) delete
    # delete 10 user


    # for user in users:
    #     if user["id"] == user_id:
    #         users.remove(user)
    #         return
    
    
