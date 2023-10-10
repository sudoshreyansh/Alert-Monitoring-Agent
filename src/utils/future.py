import asyncio

def create_new_future():
  loop = asyncio.get_running_loop()
  future = loop.create_future()
  return future