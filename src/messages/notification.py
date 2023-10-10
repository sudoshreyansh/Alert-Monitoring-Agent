from uagents import Model
from pydantic import Field
from typing import Optional


class Notification(Model):
    """
    Notification is the request sent to the Notification agent

    Args:
        Model (Model): Model from uagents

    Returns:
        Notification: Request sent to the Notification agent

    Attributes:
        phone_number (str): Phone number to send the message to
        message (str): Message to send to the user
    """
    phone_number: str = Field(
        title="Phone Number", description="Phone number to send the message to")
    message: str = Field(
        title="Message", description="Message to send to the user")
