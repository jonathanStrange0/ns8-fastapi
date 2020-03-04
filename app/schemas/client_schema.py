from pydantic import BaseModel


class Client(BaseModel):
    """
        the client object used in database
    """
    client_id: str = None
    client_name: str
