from fastapi import FastAPI
import asyncio
from uagents import Agent, Context
from pydantic import BaseModel
from agents.alerts.alert_agent import agent as alert_agent
from agents.notifications.notification_agent import agent as notification_agent
from agents.sources.source_agent import agent as source_agent
from messages.alert import AlertRequest
from utils.future import create_new_future

ALERT_AGENT_ADDRESS = alert_agent.address
NOTIFICATION_AGENT_ADDRESS = notification_agent.address
TEMPERATURE_SOURCE_AGENT_ADDRESS = source_agent.address

queue = asyncio.Queue()
app = FastAPI()
agent = Agent(
  name="backend_agent",
  seed="backend secret phase"
)

class QueueItem(BaseModel):
  location: str
  phone_number: str
  max_temperature: float
  min_temperature: float
  ack: asyncio.Future

@app.get("/api/alert")
async def add_alert(loc: str, phone: str, max_t: float, min_t: float):
  future = create_new_future()
  request = QueueItem(
    location=loc,
    phone_number=phone,
    max_temperature=max_t,
    min_temperature=min_t,
    ack=future
  )

  queue.put_nowait(request)
  response = await request.ack

  return response


# @agent.on_interval(period=1.0)
# async def handle_requests(ctx: Context):
#   try:
#     while True:
#       request = queue.get_nowait()
#       alert_request = AlertRequest(
#         source=TEMPERATURE_SOURCE_AGENT_ADDRESS,

#       )

#       queue.task_done()
#   except asyncio.QueueEmpty:
#     return


# @agent.on_message(model, repl)
# async def handle_alerts(ctx: Context, ):
