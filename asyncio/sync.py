import time

#동기(Syncronous)
# A작업 -> B 작업 

# 피호출자(callee)
def hello():
    time.sleep(3) # 3초동안 대기시킴
    print("hello")

hello() # 호출자(Caller)
