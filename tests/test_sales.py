from src.sale import Sale

def test_sale_creation():
    s = Sale("S1", 1, "Laptop", "Electronics", 999.99, "2023-01-01")
    assert s.client_id == 1
    assert s.amount == 999.99
    datos = s.to_dict()
    assert datos["sale_id"] == "S1"
    assert datos["date"] == "2023-01-01"
