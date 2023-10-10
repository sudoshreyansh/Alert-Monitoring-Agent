from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import requests
import json
import os
from dotenv import load_dotenv
import message.alert_protocol as alert_protocol
import uuid

load_dotenv()

alert = Agent(
    name="alert",
    seed="alert secret phase",
    port=8000,
    endpoint={
        "http://127.0.0.1:8000/submit": {},
    },
)
fund_agent_if_low(alert.wallet.address())

alert.include(alert_protocol, publish_manifest=True)


if _name_ == "_main_":
    alert.run()
