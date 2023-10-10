from uagents import Agent, Context, Model, Protocol
from uagents.setup import fund_agent_if_low
import requests
import json
import os
from dotenv import load_dotenv
from messages import SourceRequest, SourceResponse

# Loading environment variables
load_dotenv()


def urlBuilder(params):
    """
    urlBuilder builds the url for the API call

    Args:
        params (object): Parameters to pass to the API

    Returns:
        str: url for the API call
    """
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + \
        params.location + "&appid=" + os.getenv("API_KEY")
    return url


# Defining the Source agent
source = Agent(
    name="source",
    port=8001,
    seed="source secret phase",
    endpoint={
        "http://127.0.0.1:8001/submit": {},
    },
)

# Funding the agent
fund_agent_if_low(source.wallet.address())


# Defining the Source protocol
source_protocol = Protocol(name="SourceProtocol", version="1.0.0")

# Fetching data from the API and sending it to the Alert agent


@source_protocol.on_message(model=SourceRequest, replies=SourceResponse)
async def handle_request(ctx: Context, request: SourceRequest):
    if (request.params != ""):
        ctx.logger.info("Fetching data from API")
        try:
            data = requests.get(urlBuilder(request.params))
            data = data.json()
            ctx.logger.info("Data fetched from API")
            await ctx.send({
                "timestamp": int(time.time()),
                "data": data
            })
        except:
            ctx.logger.info("Error fetching data from API")
            await ctx.send({
                "timestamp": int(time.time()),
                "data": "Error fetching data from API"
            })
    else:
        ctx.logger.info("No parameter passed")
        ctx.send({
            "timestamp": int(time.time()),
            data: "No Parameter passed"
        })


# Sending the frequency to the Alert agent
@source_protocol.on_query()
async def handle_query(ctx: Context):
    await ctx.send(os.getenv("FREQUENCY"))

source.include(source_protocol, publish_manifest=True)

if __name__ == "__main__":
    source.run()
