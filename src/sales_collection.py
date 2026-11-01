class SalesCollection:
    def __init__(self, sales):
        self.sales = sales

# Todas las ventas de un cliente
    def  sales_by_client(self, client_id):
        lista = []
        for sale in self.sales:
            if client_id == sale.client_id:
                lista.append(sale)
        return lista

# Suma de importes de un cliente
    def total_amount_by_client(self, client_id):
        total = 0
        listaVentas=self.sales_by_client(client_id)
        for x in listaVentas:
            total += x.amount
        return total
        
# Suma de ventas de una categoría
    def total_amount_by_category(self,category):
        aux = 0
        for i in self.sales:
            if i.category == category:
                aux += i.amount 
        return aux

# Media de gasto por venta para un cliente
    def average_sale_by_client(self, client_id):
        aux = 0
        contador = 0
        for x in self.sales:
            if x.client_id == client_id:
                aux += x.amount
                contador += 1
        if contador==0: 
            return 0 
        return aux/contador
    


        