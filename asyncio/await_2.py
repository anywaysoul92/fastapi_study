

import asyncio
import time

# 1) await는 반드시 비동기 함수 안에서만 사용 가능하다
# def hello(): ❌
#     await asyncio.sleep(2)

# 2) await 할 수 있는 코드 앞에만 await를 쓸 수 있다.
async def hi():
    # await time.sleep(2) # 🔎 time.sleep은 await 할 수 있는 함수가 아니라서 오류남 
    print("start hello..")
    await asyncio.sleep(2)
    print("end hello..")

async def main():
    print("start main..")
    coro = hi()
    await coro # await 붙이는게 가능
    print("end main..")

asyncio.run(main())

# 2개 이상은 gather해야함
