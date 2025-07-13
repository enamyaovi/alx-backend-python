#!/usr/bin/env python3

import asyncio
import time

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

#writing a coroutine

async def cor_main():
    print(f"started at {time.strftime('%X')}")
    await say_after(1, 'hello')
    await say_after(2, 'World!')
    print(f"finished at {time.strftime('%X')}")

#writing coroutines that run concorruntly

async def concurrent_main():
    task1 = asyncio.create_task(say_after(1, 'hello'))
    task2 = asyncio.create_task(say_after(2, 'World!'))

    print(f"started at {time.strftime('%X')}")
    
    await task1
    await task2

    print(f"finished at {time.strftime('%X')}")

#writing concurrent with the TaskGroup Class
# Only Available In PYTHON 3.11+
# async def task_main():
    # async with asyncio.TaskGroup() as tg:
        # task1 = tg.create_task(say_after(1, 'hello!'))
        # task2 = tg.create_task(say_after(2, 'World'))
# 
        # print(f"started at {time.strftime('%X')}")
# 
    # print(f"finished at {time.strftime('%X')}")


# =============AWAITABLES=================
"""
an object is awaitable if it can use the await expression
"""
import random
my_number = random.randint(1,100)

async def nested(number):
    return number

async def nest_main():
    #nested() # will raise a runtime warning
    print(await nested(my_number))

# ========== TASKS ======================
"""
used to run coroutines concurrently
"""

async def task_main():
    task = asyncio.create_task(nested(my_number))
    await task

if __name__ == "__main__":
    import asyncio
    asyncio.run(cor_main())
    asyncio.run(concurrent_main())
    asyncio.run(nest_main())
    asyncio.run(task_main())
