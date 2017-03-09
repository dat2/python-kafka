import asyncio
import zmq
import zmq.asyncio

context = zmq.asyncio.Context()
loop = zmq.asyncio.ZMQEventLoop()
asyncio.set_event_loop(loop)

@asyncio.coroutine
def run():
  rep = context.socket(zmq.REP)
  rep.bind('tcp://*:5555')

  pub = context.socket(zmq.PUB)
  pub.bind('tcp://*:5556')

  while True:
    [topic, data] = yield from rep.recv_multipart()
    # TODO raft it up
    print('Received for topic(%s): (%s)' % (topic, data))
    reply = [b'200']
    yield from rep.send_multipart(reply)

    # send the topic to the publishers
    yield from pub.send_multipart([topic, data])

loop.run_until_complete(run())
