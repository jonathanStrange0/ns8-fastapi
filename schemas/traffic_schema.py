from pydantic import BaseModel


class TrafficAddress(BaseModel):
    """
        Desccribes an address to drive robotic traffic to \n
        client_id is an integer \n
        client: string \n
        store_address: string
    """
    client_id: int = None
    address: str
