import pandas as pd

ORDER_PATH = "data/orders.csv"

def get_order1(order_id):
    try:
        orders_df = pd.read_csv(ORDER_PATH)
    except FileNotFoundError:
        print(f"Error: The file '{ORDER_PATH}' was not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{ORDER_PATH}' is empty.")
        return None
    except pd.errors.ParserError:
        print(f"Error: The file '{ORDER_PATH}' could not be parsed.")
        return None

    order = orders_df[orders_df['order_id'] == order_id]

    if order.empty:
        print(f"No order found with ID: {order_id}")
        return None

    return order.to_dict(orient='records')[0]

