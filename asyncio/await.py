import time
import asyncio

async def a():
    print("A 작업 시작")  # 1. a실행
    await asyncio.sleep(5) # 2. 대기 -> 양보
    print("A 작업 종료")  # 5. 종료

async def b():
    print("B 작업 시작") # 3. 실행
    await asyncio.sleep(2) # 4. 대기 -> 양보
    print("B 작업 종료") # 6. 종료

async def main():
    coro1 = a()
    coro2 = b()
    await asyncio.gather(coro1, coro2)


start = time.time()
asyncio.run(main())
end = time.time()
print(f"{end - start:.2f}")