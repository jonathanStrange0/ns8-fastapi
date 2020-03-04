from fastapi import FastAPI
schemas.traffic_schema import TrafficAddress


@app.get("/traffic/{client_id}")
def update_item(client_id: int, address: TrafficAddress):
    obj = {'client_id': address.client_id, "client": address.client,
           "store_address": address.address}
    print("This object will be created: ", obj)
    print("now making request to the associated address")

    return obj


@app.post("/traffic/")
def update_item(client: Client):
    """
        docstring for post() new traffic address
    """
    db = firestore.Client()
    doc_ref = db.collection(u'clients').document(client.client_name)
    doc_ref.set({
        u'client_id': None,
        u'client_name': client.client_name
    })

    return doc_ref.get().to_dict()


@app.put("/clients/{client_id}")
def update_item(client_id: int, client: Client):
    """
        docstring for put(client_id)
    """
    # TODO: retreive a client from database and update it

    return {"Update Status": "Complete"}


@app.delete("/clients/{client_id}")
def update_item(client_id: int, client: Client):
    """
        docstring for delete(client_id)
    """
    # TODO: retreive a client from database and delete it
    return {"Delete Status": "Success"}
