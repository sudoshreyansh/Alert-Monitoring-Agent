from uagents import Model
from pydantic import Field
from typing import Optional


class SourceRequest(Model):
    """
    SourceRequest is the request sent to the Source agent

    Args:
        Model (Model): Model from uagents

    Returns:    
        SourceRequest: Request sent to the Source agent

    Attributes: 
        source (str): Source of the data
        field (str): Field to check
        params (object): Parameters to pass to the API
    """
    params: object = Field(title="Parameters", description="Parameters to pass to the API")


class SourceResponse(Model):
    """
    SourceResponse is the response sent by the Source agent

    Args:
        Model (Model): Model from uagents

    Returns:
        SourceResponse: Response sent by the Source agent

    Attributes:
        timestamp (int): Timestamp of the response
        data (object): Data from the API
    """
    timestamp: int = Field(title="Timestamp", description="Timestamp of the response")
    data: object = Field(title="Data", description="Data from the API")
