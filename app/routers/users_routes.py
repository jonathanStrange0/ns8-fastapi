from fastapi import APIRouter
from app.schemas.client_schema import Client
from app.firebase.fb_client import fb_client
router = APIRouter()
db = fb_client()

###############################################################################
##### GENERATING CLIENT INFO HERE #############################################
###############################################################################


@router.post("/clients/", tags=['clients'])
def create_client(client: Client):
    """
        docstring for post() new client
    """
    doc_ref = db.collection(
        u'clients').document(client.client_name)
    doc_ref.set({
        u'client_id': None,
        u'client_name': client.client_name
    })

    return doc_ref.get().to_dict()


@router.get("/clients/{client_id}", tags=['clients'])
def get_client(client_id: int):
    """
        docstring for get(client_id)
    """
    # TODO: retreive a client from database and return as json object

    return {"hello": "World"}


@router.put("/clients/{client_id}", tags=['clients'])
def update_client(client_ifb_clientd: int, client: Client):
    """
        docstring for put(client_id)
    """
    # TODO: retreive a client from database and update it

    return {"Update Status": "Complete"}


@router.delete("/clients/{client_id}", tags=['clients'])
def delete_client(client_id: int, client: Client):
    """
        docstring for delete(client_id)
    """
    # TODO: retreive a client from database and delete it
    return {"Delete Status": "Success"}
