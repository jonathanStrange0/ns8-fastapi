from pydantic import BaseModel


class Utm_Parameters(BaseModel):
    """
    A short description.

    A bit longer description.

    Args:
        variable (type): description

    Returns:
        type: description

    Raises:
        Exception: description

    """

    # url template: jonathanmucha.me?utm_source=source&utm_medium=medium&utm_campaign=name
    campaign_source: str
    campaign_medium: str
    campaign_name: str
