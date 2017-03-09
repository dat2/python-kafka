import asyncio
import zmq
import zmq.asyncio
import random

def get_random_choice():
  return random.choice([b'X', b'Y'])

context = zmq.asyncio.Context()
loop = zmq.asyncio.ZMQEventLoop()
asyncio.set_event_loop(loop)

@asyncio.coroutine
def run():
  req = context.socket(zmq.REQ)
  req.connect('tcp://localhost:5555')
  for i in range(10):
    yield from req.send_multipart([get_random_choice(), str(i).encode()])
    reply = yield from req.recv_multipart()
    print(reply)

loop.run_until_complete(run())
