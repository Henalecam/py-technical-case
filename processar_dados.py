import json
from collections import defaultdict, Counter


def load_json(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if not isinstance(data, list):
                raise ValueError(f"Arquivo '{filename}' deve conter um array JSON.")
            return data
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo '{filename}' não encontrado.")
    except json.JSONDecodeError as e:
        raise ValueError(f"JSON inválido no arquivo '{filename}': {e}")


def validate_required_fields(item, required_fields, item_type='Item'):
    for field in required_fields:
        if field not in item:
            raise ValueError(f"{item_type} faltando o campo '{field}'.")


def validate_numeric_value(value, field_name, min_value=0):
    if not isinstance(value, (int, float)) or value < min_value:
        raise ValueError(f"Valor inválido para o campo '{field_name}': {value}")


def merge_data(customers, orders):
    if not customers:
        raise ValueError("Lista de clientes está vazia.")
    if not orders:
        raise ValueError("Lista de pedidos está vazia.")
    
    customers_by_id = {}
    for customer in customers:
        validate_required_fields(customer, ['id', 'name', 'country'], 'Customer')
        customers_by_id[customer['id']] = customer
    
    complete_orders = []
    for order in orders:
        validate_required_fields(order, ['client_id'], 'Order')
        
        client_id = order['client_id']
        if client_id not in customers_by_id:
            continue
        
        customer = customers_by_id[client_id]
        complete_order = {**order, 'customer_name': customer['name'], 'country': customer['country']}
        complete_orders.append(complete_order)
    
    if not complete_orders:
        raise ValueError("Nenhum pedido válido encontrado após mesclar com clientes.")
    
    return complete_orders


def generate_report(orders):
    if not orders:
        raise ValueError("Não é possível gerar relatório a partir de uma lista de pedidos vazia.")
    
    orders_per_customer = Counter(order['customer_name'] for order in orders)
    revenue_by_country = defaultdict(float)
    quantity_by_product = Counter()
    total_spent_by_customer = defaultdict(float)
    
    for order in orders:
        validate_required_fields(order, ['quantity', 'price', 'country', 'product', 'customer_name'], 'Order')
        
        quantity = order['quantity']
        price = order['price']
        validate_numeric_value(quantity, 'quantity')
        validate_numeric_value(price, 'price')
        
        revenue = quantity * price
        revenue_by_country[order['country']] += revenue
        quantity_by_product[order['product']] += quantity
        total_spent_by_customer[order['customer_name']] += revenue
    
    if not quantity_by_product:
        raise ValueError("Nenhum produto encontrado nos pedidos.")
    if not total_spent_by_customer:
        raise ValueError("Nenhum dado de gasto por cliente encontrado.")
    
    best_product_name, best_product_quantity = quantity_by_product.most_common(1)[0]
    top_customer_name, top_customer_spent = max(total_spent_by_customer.items(), key=lambda item: item[1])
    
    return {
        'total_orders_per_customer': dict(orders_per_customer),
        'total_revenue_per_country': dict(revenue_by_country),
        'best_selling_product': {
            'product': best_product_name,
            'total_quantity': best_product_quantity
        },
        'top_spending_customer': {
            'customer': top_customer_name,
            'total_spent': top_customer_spent
        }
    }


def save_report(report, filename='relatorio.json'):
    if not report:
        raise ValueError("Não é possível salvar um relatório vazio.")
    
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(report, file, ensure_ascii=False, indent=2)
    except OSError as e:
        raise OSError(f"Erro ao escrever o arquivo '{filename}': {e}")


def main():
    try:
        customers = load_json('clientes.json')
        orders = load_json('pedidos.json')
        
        complete_orders = merge_data(customers, orders)
        report = generate_report(complete_orders)
        
        save_report(report)
    except (FileNotFoundError, ValueError, OSError) as e:
        print(f"Erro: {e}")
        return 1
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    main()

