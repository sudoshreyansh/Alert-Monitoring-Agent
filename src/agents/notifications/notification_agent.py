from twilio.rest import Client
from uagents import Agent, Context, Model
from uagents.setup import fund_agent_if_low
from dotenv import load_dotenv
import os
from message import Notification

# Your Account Sid and Auth Token from twilio.com/console
client = Client(os.getenv("ACCOUNT_SID"), os.getenv("AUTH_TOKEN"))
NOTIIFICATION_AGENT_SEED = os.getenv("NOTIFICATION")

# Loading environment variables
load_dotenv()


async def notify_user(phone_number, message):
    """
    notify_user sends a message to a user

    Args:
        phone_number (str): Phone number to send the message to
        message (str): Message to send to the user

    Returns:
        bool: True if the message was sent successfully, False otherwise
    """
    try:
        await client.messages.create(
            body=message,
            from_=os.getenv(PHONE_NUMBER),
            to=phone_number
        )
        return True
    except:
        return False


# Defining the Notification agent
notification = Agent(
    name="Notification",
    seed=NOTIIFICATION_AGENT_SEED,
    port=8002,
    endpoint={
        "http://127.0.0.1:8002/submit": {},
    },
)

# Funding the agent
fund_agent_if_low(notification.wallet.address())


# Defining the Notification protocol
@notification.on_message(Notification)
async def notify_user(ctx: Context,  sender: str, msg: Notification):
    status = notify_user(msg.phone_number, msg.message)
    ctx.send(sender, status)


if __name__ == "__main__":
    notification.run()
