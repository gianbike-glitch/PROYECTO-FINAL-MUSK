class ClientCollection:
    def __init__(self, clients):
        self.clients = clients

    def  get_client_by_id(self, client_id):
        for client in self.clients:
            if client_id == client.client_id:
                return client
        