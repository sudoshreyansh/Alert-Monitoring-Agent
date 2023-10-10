from fastapi import FastAPI
import asyncio
from uagents import Agent, Context
from pydantic import BaseModel
from agents.alerts.alert_agent import agent as alert_agent
from agents.notifications.notification_agent import agent as notification_agent
from agents.sources.source_agent import agent as source_agent
from messages.alert import AlertRequest, AlertResponse
from messages.notification import Notification
from uagents.query import query

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

@app.get("/api/alert")
async def add_alert(loc: str, phone: str, max_t: float, min_t: float):
  request = QueueItem(
    location=loc,
    phone_number=phone,
    max_temperature=max_t,
    min_temperature=min_t,
  )

  queue.put_nowait(request)
  return {'success': True}


@agent.on_interval(period=1.0)
async def handle_requests(ctx: Context):
  try:
    while True:
      request = queue.get_nowait()
      envelope = await query(ALERT_AGENT_ADDRESS, AlertRequest(
        source=TEMPERATURE_SOURCE_AGENT_ADDRESS,
        field="main.temperature",
        params={
          "q": request.location
        },
        threshold=request.max_temperature
      ))
      alert = envelope.decode_payload().id

      ctx.storage.set(alert, request.phone_number)
      queue.task_done()
  except asyncio.QueueEmpty:
    return

@agent.on_message(model=AlertResponse)
async def handle_alerts(ctx: Context, sender: str, message: AlertResponse):
  phone_number = ctx.storage.get(message.id)
  await ctx.send(NOTIFICATION_AGENT_ADDRESS, Notification(
    phone_number=phone_number,
    message="The current temperature crossed the threshold temperature."
  ))