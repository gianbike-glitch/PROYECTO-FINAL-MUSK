class SalesCollection:
    def __init__(self, sales):
        self.sales = sales

    def  sales_by_client(self, client_id):
        lista = []
        for sale in self.sales:
            if client_id == sale.client_id:
                lista.append(sale)
        return lista

    def total_amount_by_client(self, client_id):
        total = 0
        listaVentas=self.sales_by_client(client_id)
        for x in listaVentas:
            total += x.amount
        return total
        
            

        