from twilio.rest import Client
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from dotenv import load_dotenv
import os

fund_agent_if_low(Notification.wallet.address())
client = Client(os.getenv("ACCOUNT_SID"), os.getenv("AUTH_TOKEN"))

load_dotenv()


class Message(Model):
    phone_number: str
    message: str


async def notify_user(phone_number, message):
    try:
        await client.messages.create(
            body=message,
            from_=os.getenv(PHONE_NUMBER),
            to=phone_number
        )
        return True
    except:
        return False


Notification = Agent(
    name="Notification",
    seed="Notification secret phrase",
    port=8002,
    endpoint={
        "http://127.0.0.1:8002/submit": {},
    },
)


@Notification.on_message(Message)
async def log_msg(ctx: Context,  sender: str, msg: Message):
    status = notify_user(msg.phone_number, msg.message)
    ctx.send(sender, status)


if _name == "main_":
    Notification.run()
