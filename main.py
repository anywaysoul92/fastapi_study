from fastapi import FastAPI
from user.router import router 
import anyio # fastapi 안에 들어가는 엔진을 갈아끼울 수 있다. 추상화된 레이어 표준은 asyncio임
from contextlib import asynccontextmanager
from starlette.concurrency import run_in_threadpool
# 비동기를 지원하지 않기 때문에 강제로 thread pool에 넣어주는 라이브러리 



# 쓰레드 풀 크기 조정
@asynccontextmanager
async def lifespan(_):
    limiter = anyio.to_thread.current_default_thread_limiter()
    limiter.total_token =200 # Thread pool 조정하는 표준 보퉁 100~200 괜찮은 둣
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(router)

# 비동기 라이브러리를 지원하지 않는 경우

def aws_sync():
    #AWS 서버랑 통신(예:2초)
    return

@app.get("/async")
async def async_handler():
    # 동기 함수를 비동기 방식으로 실행 할 수 있게 해주는 유틸리티 함수 
    await run_in_threadpool(aws_sync)
    return {"mag": "ok"}