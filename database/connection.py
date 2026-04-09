# SQLAlchemy 를 이용해서 DB와 연결하는 코드 
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 데이터베이스 접속
DATABASE_URL = "sqlite:///./local.db"

# Engine: DB와 접속을 관리하는 객체 
engine = create_engine(DATABASE_URL, echo=True)
#echo=True 알아서 만드는 sql을 보여준다

# Session : 한번의 DB 요청-응답 단위 
# SessionFactory 엔진으로 공장을 먼저 만듦 
SessionFactory = sessionmaker(
    bind=engine,
    #데이터를 어떻게 다룰지를 조정하는 옵션
    # ( False 자동화를 끄는 이유는 제어할 수 없는 부분에서 문제가 발생하면
    #  조절할 수 없어서  하지만 사용자가 원하는 방식으로 해도됨 )
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)

# SQLAlchemy 세션을 관리하는 함수 
def get_session():
    session = SessionFactory()
    
    try:
    # 일시정지
        yield session
    finally:
        session.close()


