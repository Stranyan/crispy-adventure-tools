import subprocess
import asyncio
import time

async def ping(last_octect):
    ip = '172.16.1.%s' % last_octect
    await asyncio.create_subprocess_exec('ping', '-n', '1', '-w', '1', ip, stdout=asyncio.subprocess.PIPE)

async def main():
    tasks = []
    for i in range(1, 255):
        tasks.append(ping(i))
    await asyncio.gather(*tasks)

start_time = time.time()
loop = asyncio.ProactorEventLoop()
asyncio.set_event_loop(loop)
loop.run_until_complete(main())
loop.close()
print('总共耗时: %.2f' % (time.time() - start_time))
