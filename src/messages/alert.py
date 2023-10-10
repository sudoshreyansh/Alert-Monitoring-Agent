from uagents import Model
from pydantic import Field
from typing import Optional


class AlertRequest(Model):
    """
    AlertRequest is the request sent to the Alert agent

    Args:
        Model (Model): Model from uagents

    Returns:
        AlertRequest: Request sent to the Alert agent

    Attributes:
        source (str): Source of the data
        field (str): Field to check
        params (object): Parameters to pass to the API
        threshold (int): Threshold to check
    """
    source: str = Field(title="Source", description="Source of the data")
    field: str = Field(title="Field", description="Field to check")
    params: object = Field(
        title="Parameters", description="Parameters to pass to the API")
    threshold: int = Field(title="Threshold", description="Threshold to check")


class AlertResponse(Model):
    """
    AlertResponse is the response sent by the Alert agent

    Args:
        Model (Model): Model from uagents

    Returns:
        AlertResponse: Response sent by the Alert agent

    Attributes:
        status (bool): Status of the alert
    """
    id: str = Field(title="ID", description="ID of the alert")


class DeleteAlertRequest(Model):
    """
    DeleteAlertRequest is the request sent to the Alert agent to delete an alert

    Args:
        Model (Model): Model from uagents

    Returns:
        DeleteAlertRequest: Request sent to the Alert agent to delete an alert

    Attributes:
        id (str): ID of the alert
    """
    id: str = Field(title="ID", description="ID of the alert")


class DeleteAlertResponse(Model):
    """
    DeleteAlertResponse is the response sent by the Alert agent after deleting an alert

    Args:
        Model (Model): Model from uagents

    Returns:
        DeleteAlertResponse: Response sent by the Alert agent after deleting an alert

    Attributes:
        status (bool): Status of the deletion
    """
    status: bool = Field(title="Status", description="Status of the deletion")
