from src.agents.backend.backend_agent import app as backend_api, agent as backend_agent
from uagents import Bureau
import uvicorn
import threading
import asyncio
import time


def setup_agents():
  asyncio.set_event_loop(asyncio.new_event_loop())
  bureau = Bureau()
  bureau.add(backend_agent)
  bu
  bureau.run()

def setup_server():
  uvicorn.run("main:backend_api", port=5000, log_level="info")
    

if __name__ == "__main__":
  t1 = threading.Thread(target=setup_agents)
  t2 = threading.Thread(target=setup_server)

  t1.setDaemon(True)
  t2.setDaemon(True)

  t1.start()
  t2.start()

  while True:
    time.sleep(1)
