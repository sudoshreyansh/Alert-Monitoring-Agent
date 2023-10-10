from uagents import Agent, Context, Model, Protocol
from uagents.setup import fund_agent_if_low
import requests
import json
import os
from dotenv import load_dotenv
from uagents.query import query
from uagents.contrib.protocols.protocol_query import ProtocolQuery, ProtocolResponse
from messages import SourceRequest, AlertRequest, AlertResponse, DeleteAlertRequest, DeleteAlertResponse
import uuid

# Loading environment variables
load_dotenv()

# Global variables
ALERTS = {}
CALLS = {}

# Defining the Alert agent
alert = Agent(
    name="alert",
    seed="alert secret phase",
    port=8000,
    endpoint={
        "http://127.0.0.1:8000/submit": {},
    },
)

# Funding the agent
fund_agent_if_low(alert.wallet.address())

# Defining the Alert protocol
alert_protocol = Protocol(name="AlertProtocol", version="1.0.0")


# Defining the Alert protocol handlers
# Handle Alert Request and create a New Alert
@alert.on_message(model=AlertRequest, replies=AlertResponse)
async def handle_alert_request(ctx: Context, sender: str, msg: Alert):
    id = str(uuid.uuid4())
    freq = await query(sender)
    alert = {
        "id": id,
        "field": msg.field,
        "source": msg.source,
        "threshold": msg.threshold,
        "params": msg.params,
        "frequency": freq
    }
    if (sender in ALERTS):
        ALERTS[sender].append(alert)
    else:
        ALERTS[msg.type] = [alert]
    ctx.logger.info("Alert Created")
    await ctx.send(AlertResponse(id=id))


# Handle Delete Alert Request and delete an Alert
@alert.on_message(model=DeleteAlertRequest, replies=DeleteAlertResponse)
async def handle_delete_alert_request(ctx: Context, sender: str, msg: DeleteAlertRequest):
    for alert in ALERTS[sender]:
        if alert["id"] == msg.id and alert["user"] == sender:
            ctx.logger.info("Alert Deleted")
            ALERTS[sender].remove(alert)
            await ctx.send(DeleteAlertResponse(status=True))
        else:
            ctx.logger.info("Alert not found")
            await ctx.send(DeleteAlertResponse(status=False))


# Handle Interval and check for Alerts
@alert.on_interval(period=os.getenv("FREQUENCY"))
async def handle_interval(ctx: Context):
    for user in ALERTS:
        for alert in ALERTS[user]:
            if (not CALLS[alert["id"]]):
                CALLS[alert["id"]] = time.time()
            time = CALLS[alert["id"]]
            if (time.time() - time < alert["frequency"]):
                continue
            queryToSource = await query(ALERTS[alert]["source"], SourceRequest({params: {location: ALERTS[alert]["params"]["location"]}}))
            dataValue = ProtocolResponse.parse_raw().json()[
                ALERTS[alert]["field"]]
            if int(alert["threshold"]) > int(dataValue):
                ctx.logger.info("Alert Triggered")
                await query(user, AlertResponse({id: alert["id"]}))
                CALLS[alert["id"]] = time.time()
            else:
                pass

alert.include(alert_protocol)

if __name__ == "__main__":
    alert_protocol.start()
