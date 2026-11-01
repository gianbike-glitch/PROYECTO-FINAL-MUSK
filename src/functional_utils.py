# SUMA TOTAL VENTAS CSV
def calculate_total(importes):
    return sum(importes)

# MEDIA DE LAS VENTAS TOTALES
def calculate_average(importes):
    if len(importes) == 0:
        return 0
    
    total = calculate_total(importes)
    media = total/len(importes)
    return media

# CUENTA EL NUMERO TOTAL DE VENTAS
def count_sales(ventas):
    return len(ventas)

# FILTRA LAS VENTAS MAYORES A 500
def filter_high_amounts(importes):
    return list(filter(lambda importe: importe > 500, importes))


# FILTRA LAS VENTAS POR CATEGORÍA
def filter_sales_by_category(sales, category):
    return list(
        filter(
            lambda sale: sale.category == category,
            sales
        )
    )

