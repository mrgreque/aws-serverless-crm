from datetime import datetime

# function to calculate the discount based on the value and the discount type
def calculate_discount(value, discount):
    if discount is None:
        return 0
    elif discount.endswith("%"):
        discount = float(discount[:-1]) / 100
        return value * discount
    elif discount.startswith("R$"):
        discount = float(discount[2:].replace(",", ".")).__round__(2)
        return discount
    else:
        return 0
    
# function to format the date from ERP to CRM format
def format_date(date):
    return datetime.strptime(date, "%d/%m/%Y").strftime("%Y-%m-%d")

# function to transform the data from ERP to CRM format
def transform_data(erp_data):
    map_status = {
        'finished': 'concluido',
        'in progress': 'aberto',
        'cancelled': 'cancelado',
        'other': 'outro'
    }
    transformed_data = []

    for item in erp_data:
        item["data"] = format_date(item["data"])
        item["status"] = map_status[item["status"]] if item["status"] in map_status else "outro"
        item["desconto"] = calculate_discount(item["valor"], item["desconto"])

        transformed_data.append({
            "id": str(item["id"]),
            "origem": "crm-data",
            "data_fato": item["data"],
            "status": "finalizado",
            "valor": item["valor"], 
            "desconto": item["desconto"],
            "frete": item["frete"]
        })
    return transformed_data