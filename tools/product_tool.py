import pandas as pd
from pathlib import Path

PRODUCT_PATH = Path("data/products.csv")

def search_products(
        query: str = "",
        category: str = "",
        max_price: int | None = None,
        min_rating: float | None = None
):
    try:
        products_df = pd.read_csv(PRODUCT_PATH)

    except FileNotFoundError:
        return "The products file was not found"

    except pd.errors.EmptyDataError:
        return "The products files is empty"

    except pd.errors.ParserError:
        return "The products file couold not be parse"

    results = products_df.copy()

    if category:
        results = results[
            results["category"].str.lower() == category.lower()
        ]

    if max_price is not None:
        results = results[
            results["price"] <= max_price 
        ]

    if min_rating is not None:
        results = results[
            results["rating"] >= min_rating
        ]

    # Text search
    if query:
        query = query.lower()

        results = results[
            results["product_name"].str.contains(query,case=False, na=False)
            |
            results["description"].str.contains(query,case=False, na=False)
        ]

    if results.empty:
        return "No Products matched the given requiremnts."

    return results.to_dict(orient="records")

def print_products(products):
    if isinstance(products, str):
        print(products)
        return

    if not products:
        print("No products found.")
        return

    for product in products:
        print(f"\nProduct ID: {product['product_id']}")
        print(f"Name: {product['product_name']}")
        print(f"Category: {product['category']}")
        print(f"Price: ${product['price']}")
        print(f"Stock: {product['stock']}")
        print(f"Rating: {product['rating']}")
        print(f"Description: {product['description']}")

if __name__ == "__main__":
    result = search_products(
        category="Laptop",
        max_price=800,
        min_rating=4
    )

    print_products(result)