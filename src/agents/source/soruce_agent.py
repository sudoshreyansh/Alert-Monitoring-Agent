from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
import requests
import json
import os
from dotenv import load_dotenv
import message.source_protocol as source_protocol

load_dotenv()

source = Agent(
    name="source",
    port=8001,
    seed="source secret phase",
    endpoint={
        "http://127.0.0.1:8001/submit": {},
    },
)
fund_agent_if_low(source.wallet.address())
source.include(source_protocol, publish_manifest=True)

if _name_ == "_main_":
    source.run()
