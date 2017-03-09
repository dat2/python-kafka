import asyncio
import zmq
import zmq.asyncio
import sys

context = zmq.asyncio.Context()
loop = zmq.asyncio.ZMQEventLoop()
asyncio.set_event_loop(loop)

@asyncio.coroutine
def run():
  sub = context.socket(zmq.SUB)
  sub.connect('tcp://localhost:5556')

  sub.setsockopt_string(zmq.SUBSCRIBE, sys.argv[1])

  while True:
    msg = yield from sub.recv_multipart()
    print(msg)

loop.run_until_complete(run())
