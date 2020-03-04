from pydantic import BaseModel


class OrderAddress(BaseModel):
    """
        Desccribes an address to drive robotic traffic to \n
        client_id is an integer \n
        client: string \n
        store_address: string
    """
    client_id: int = None  # Going to remove None here later when the frontend provides the user
    client: str
    address: str
