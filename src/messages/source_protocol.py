from uagents import Context, Model, Protocol
import os
from dotenv import load_dotenv

load_dotenv()


source_protocol = Protocol(name="SourceProtocol", version="1.0.0")


class SourceRequest(Model):
    params: object


class SourceResponse(Model):
    timestamp: int
    data: object


def urlBuilder(params):
    url = "https://api.openweathermap.org/data/2.5/weather?q=" + \
        params.location + "&appid=" + os.getenv("API_KEY")
    return url


@source_protocol.on_message(model=SourceRequest, replies=SourceResponse)
async def handle_request(ctx: Context, request: SourceRequest):
    if (request.params != ""):
        ctx.logger.info("Fetching data from API")
        try:
            data = requests.get(urlBuilder(request.params))
            data = data.json()
            ctx.logger.info("Data fetched from API")
            await ctx.send({
                "data": data
            })
        except:
            ctx.logger.info("Error fetching data from API")
            await ctx.send({
                "data": "Error fetching data from API"
            })
    else:
        ctx.logger.info("No parameter passed")
        ctx.send({
            data: "No Parameter passed"
        })


@source_protocol.on_query()
async def handle_query(ctx: Context):
    await ctx.send(os.getenv("FREQUENCY"))
