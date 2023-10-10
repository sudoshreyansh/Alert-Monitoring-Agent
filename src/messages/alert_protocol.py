from uagents import Context, Model, Protocol
from uagents.query import query
from uagents.contrib.protocols.protocol_query import ProtocolQuery, ProtocolResponse
from messages.source_protocol import SourceRequest, SourceResponse

alert_protocol = Protocol(name="AlertProtocol", version="1.0.0")


ALERTS = {}


class AlertRequest(Model):
    source: str
    field: str
    params: object
    threshold: int


class AlertResponse(Model):
    id: str


class DeleteAlertRequest(Model):
    id: str


class DeleteAlertResponse(Model):
    status: bool


@alert.on_message(model=AlertRequest, replies=AlertResponse)
async def handle_alert_request(ctx: Context, sender: str, msg: Alert):
    id = str(uuid.uuid4())
    alert = {
        "id": id,
        "field": msg.field,
        "source": msg.source,
        "threshold": msg.threshold,
        "params": msg.params,
    }
    if (sender in ALERTS):
        ALERTS[sender].append(alert)
    else:
        ALERTS[msg.type] = [alert]
    ctx.logger.info("Alert Created")
    await ctx.send(AlertResponse(id=id))


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


@alert.on_interval(period=os.getenv("FREQUENCY"))
async def handle_interval(ctx: Context):
    for user in ALERTS:
        for alert in ALERTS[user]:
            queryToSource = await query(ALERTS[alert]["source"], SourceRequest({params: {location: ALERTS[alert]["params"]["location"]}}))
            dataValue = ProtocolResponse.parse_raw().json()[
                ALERTS[alert]["field"]]
            if int(alert["threshold"]) > int(dataValue):
                ctx.logger.info("Alert Triggered")
                await query(user, AlertResponse({id: alert["id"]}))
            else:
                pass
