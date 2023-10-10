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
  agents_thread = threading.Thread(target=setup_agents)
  http_thread = threading.Thread(target=setup_server)

  agents_thread.setDaemon(True)
  http_thread.setDaemon(True)

  agents_thread.start()
  http_thread.start()

  while True:
    time.sleep(1)
