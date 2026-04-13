# 🚀 FastAPI & SQLAlchemy Study Project

FastAPI의 비동기(`asyncio`) 처리 메커니즘과 SQLAlchemy ORM을 활용한 데이터베이스 설계를 깊이 있게 학습하는 저장소입니다.

---

## 🛠 Tech Stack
* **Framework:** FastAPI
* **ORM:** SQLAlchemy (Async/Sync)
* **Database:** SQLite (local.db)
* **Language:** Python 3.14

---

## 📂 Project Structure
* **asyncio**: 비동기 프로그래밍 기초 (await, coroutine, blocking 테스트)
* **database**: DB 연결 설정 및 Async Session 관리
* **user**: 사용자 도메인 (Models, Router, Request/Response Schema)
* **main.py**: 애플리케이션 진입점

---

## ⚙️ How to Run
1. **가상환경 생성 및 활성화**
   ```bash
   python -m venv venv
   Windows: venv\Scripts\activate
   
2. **패키지 설치**

3. **서버 실행**
---

## 📝 Key Learning Points

### 1. Async & Await Workflow (적재적소의 비동기)
* async/await를 적재적소에 배치하여 I/O 대기 시간을 줄이고 시스템 자원을 효율적으로 사용하는 방법을 익혔습니다.
* 리스크 관리: 특히 이벤트 루프(Event Loop) 블로킹이 발생하지 않도록 주의하며, CPU 집약적인 작업과 I/O 작업의 분리 중요성을 학습했습니다. ⭐

### 2. Pythonic Database Handling (SQLAlchemy)
* 직접적인 SQL 쿼리 대신 파이썬 언어(ORM)를 사용하여 데이터를 조회하는 방식의 편리함을 경험했습니다.
* 번거로운 문자열 쿼리 작성 시간을 줄이고, 파이썬의 타입 힌트와 객체 지향적 특성을 활용해 데이터 가독성을 높였습니다.
* `scalars()`, `mappings()`, `all()` 메서드를 구현했습니다. 
* **scalars()**: 단일 객체 조회 시 객체를 꺼내오기 위해서 사용.
* **mappings()**: Key-Value 즉 dict. 형태의 결과가 필요할 때 사용

### 3. Result Handling & Optimization
scalars(), mappings(), all() 메서드를 통해 상황에 맞는 최적의 데이터 추출 방식을 적용했습니다.
혼동 원인: scalars()가 첫 줄이 아닌 각 행의 첫 번째 열을 가져온다는 점을 명확히 구분하여 데이터 유실 리스크를 방지했습니다. 

### 4. Dependency Injection (DI)
* `SessionFactory`를 직접 호출하지 않고, FastAPI의 `Depends`를 통해 의존성을 DB 세션을 주입받아 **결합도를 낮추는 설계**를 적용했습니다.




