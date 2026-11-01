import json
import pandas as pd
from pathlib import Path
from src.functional_utils import (
    calculate_total,
    calculate_average,
    count_sales,
    filter_sales_by_category
)

from src.client import Client
from src.sale import Sale
from src.client_collection import ClientCollection
from src.sales_collection import SalesCollection



def load_data():
    base_dir = Path(__file__).resolve().parent.parent

    clients_path = base_dir / "data" / "clients.json"
    sales_path = base_dir / "data" / "sales.csv"

    with open(clients_path, "r", encoding="utf-8") as file:
        clients = json.load(file)

    sales = pd.read_csv(sales_path)

    return clients, sales



def generate_report():
    clients, sales = load_data()

    # Crear objetos Client
    client_objects = [
        Client(
            client["client_id"],
            client["name"],
            client["country"],
            client["signup_date"]
        )
        for client in clients
    ]

    # Crear objetos Sale
    sale_objects = [
        Sale(
            row.sale_id,
            int(row.client_id),
            row.product,
            row.category,
            float(row.amount),
            row.date
        )
        for row in sales.itertuples(index=False)
    ]

    # Crear las colecciones
    client_collection = ClientCollection(client_objects)
    sales_collection = SalesCollection(sale_objects)

    # Crear DataFrame de clientes
    clients_df = pd.DataFrame(
        [client.to_dict() for client in client_objects]
    )

    merged_sales = pd.merge(
        clients_df,
        sales,
        on="client_id"
    )
    
    # 1. Número total de clientes
    total_clients = len(clients)

    # 2. Número total de ventas
    total_sales = count_sales(sales.to_dict("records"))

    # Ingresos totales
    total_revenue = calculate_total(sales["amount"].tolist())

    # 3, 4, 5. Cálculos por cliente
    clients_report = []

    for client in clients:
        client_id = client["client_id"]

        # Filtrar las ventas del cliente
        # Buscar el cliente y sus ventas usando las colecciones
        client_object = client_collection.get_client_by_id(client_id)
        client_sales = sales_collection.sales_by_client(client_id)

        amounts = [sale.amount for sale in client_sales]

        total_spent = calculate_total(amounts) 
        sale_count = count_sales(amounts)
        average_sale = calculate_average(amounts)

        clients_report.append({
            "client_id": client_id,
            "name": client_object.name,
            "total_spent": round(total_spent, 2),
            "sale_count": sale_count,
            "average_sale": round(average_sale, 2)
        })


    # 6. Cliente que más ha gastado en cada país
    top_client_by_country = {}

    for client in client_objects:
        country = client.country

        # Obtener los clientes de ese país
        clients_in_country = client_collection.clients_by_country(country)

        for client_country in clients_in_country:
            total_spent = sales_collection.total_amount_by_client(
                client_country.client_id
            )

            if country not in top_client_by_country:
                top_client_by_country[country] = {
                    "name": client_country.name,
                    "total_spent": total_spent
                }

            elif total_spent > top_client_by_country[country]["total_spent"]:
                top_client_by_country[country] = {
                    "name": client_country.name,
                    "total_spent": total_spent
                }

    top_client_by_country = {
        country: data["name"]
        for country, data in top_client_by_country.items()
    }

    # 7. Total de ventas por categoría
    sales_by_category = (
        merged_sales.groupby("category")["amount"]
        .sum()
        .round(2)
        .to_dict()
    )
    
    # 8. Cliente con más ventas en una categoría específica
    ventas_electronicas = filter_sales_by_category(
        sale_objects,
        "Electronics"
    )

    ventas_por_cliente = {}

    for client in client_objects:
        ventas_cliente = [
            sale for sale in ventas_electronicas
            if sale.client_id == client.client_id
        ]

        ventas_por_cliente[client.name] = count_sales(ventas_cliente)

    cliente_mas_ventas = max(
        ventas_por_cliente,
        key=ventas_por_cliente.get
    )

    print(ventas_por_cliente)
    print(cliente_mas_ventas)

    #9 Número de clientes que superan los 500 €
    high_spending_clients = list(map(
        lambda client: client["name"],
        filter(
            lambda client: client["total_spent"] > 500,
            clients_report
        )
    ))
   
    number_high_spending_clients = count_sales(
        high_spending_clients
    )

    print(number_high_spending_clients)

    # 10 Totales agrupados por mes (YYYY-MM)
    sales["date"] = pd.to_datetime(sales["date"])
    sales["month"] = sales["date"].dt.to_period("M").astype(str)

    monthly_sales = (
        sales.groupby("month")["amount"]
        .sum()
        .round(2)
        .to_dict()
    )

    report = {
        "summary": {
            "total_clients": total_clients,
            "total_sales": total_sales,
            "total_revenue": round(float(total_revenue), 2)
        },
        "clients": clients_report,
        "sales_by_category": sales_by_category,
        "top_client_by_country": top_client_by_country,
        "high_spending_clients": high_spending_clients,
        "monthly_sales":monthly_sales
    }

    return report

if __name__ == "__main__":
    report = generate_report()

    base_dir = Path(__file__).resolve().parent.parent
    report_path = base_dir / "data" / "report.json"

    with open(report_path, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4, ensure_ascii=False)

    print(f"Informe generado en: {report_path}")
