import asyncio
import zmq
import zmq.asyncio
import random

# 3 states
# follower
# candidate
# leader

# LEADER ELECTION
# all nodes start in FOLLOWER state
# follower waits ELECTION_TIMEOUT until becoming a CANDIDATE
  # randomized between 150 - 300 ms
# follower becomes candidate, starts new ELECTION TERM
# sends REQUEST_VOTE to all others
  # REQUEST_VOTE 1
  # if have not voted in this ELECTION_TERM, REPLY_VOTE 1
# candidate waits ELECTION_TIMEOUT and resets it when it receives a majority of votes
# candidate becomes leader if it gets majority votes

# LOG REPLICATION
# leader replicates to followers
  # APPEND_ENTRY <index> <data>
  # ACK_APPEND_ENTRY <index>
# after a majority of ACK have been received, then commit entry
# notify commit
  # COMMIT_LOG_ENTRY <index>

FOLLOWER = 0
CANDIDATE = 1
LEADER = 2

def election_timeout():
  return random.randint(150, 300) / 1000.0

async def wait_for_election_term(state_frontend):
  done, pending = await asyncio.wait(
    [ asyncio.sleep(election_timeout()), state_frontend.recv_multipart() ],
    return_when = asyncio.FIRST_COMPLETED)

  print(done)
  print(pending)

context = zmq.asyncio.Context()
loop = zmq.asyncio.ZMQEventLoop()
asyncio.set_event_loop(loop)

async def run(state_port = '5557', others = []):
  # client_frontend = context.socket(zmq.REP)
  # client_frontend.bind('tcp://*:5555')

  # pub_backend = context.socket(zmq.PUB)
  # pub_backend.bind('tcp://*:5556')

  # create the state sockets
  state_backend = context.socket(zmq.PUB)
  state_backend.bind('tcp://*:%s' % state_port)

  state_frontend = context.socket(zmq.SUB)
  for other in others:
    state_frontend.connect('tcp://%s' % other)

  # start in FOLLOWER state
  state = FOLLOWER
  await wait_for_election_term(state_frontend)

  # publish a REQUEST_VOTE message

  # while True:
  #   [topic, ...data] = yield from rep.recv_multipart()
  #   # TODO raft it up
  #   print('Received for topic(%s): (%s)' % (topic, data))
  #   reply = [b'200']
  #   yield from rep.send_multipart(reply)

  #   # send the topic to the publishers
    # yield from pub.send_multipart([topic, data])

def main():
  loop.run_until_complete(run())
  loop.close()

if __name__ == '__main__':
  main()
