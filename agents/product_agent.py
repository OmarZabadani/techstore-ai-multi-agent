from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_agent
import warnings

warnings.filterwarnings(
    "ignore",
    message="Model 'geminin-3.6-flash' uses fixed sampling defaults*"
)

from tools.product_tool import search_products

from dotenv import load_dotenv

load_dotenv()


@tool
def search_product_catalog(
    query: str = "",
    category: str = "",
    max_price: int | None = None,
    min_rating: float | None = None,
) -> str:
    """Search the TechStore product catalog using product requirements."""

    products = search_products(
        query=query,
        category=category,
        max_price=max_price,
        min_rating=min_rating,
    )

    if isinstance(products, str):
        return products

    if not products:
        return "No products matched the customer's requirements."

    return str(products)


llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)


tools = [
    search_product_catalog
]


system_prompt = """
You are the TechStore Product Agent.

Your job is to help customers with products available in the TechStore
product catalog.

You can:
- Search for products.
- Provide product details.
- Provide product specifications.
- Provide prices.
- Check stock availability.
- Recommend products based on the customer's requirements.

Use the search_product_catalog tool whenever you need information
about products.

When recommending products, consider the customer's:
- Category
- Budget
- Rating requirements
- Product specifications
- Other requirements mentioned by the customer

Never invent product information.

Only provide product information that comes from the product catalog.

Give clear and helpful answers.
"""


product_agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)


def get_product_answer(question: str) -> str:
    response = product_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )

    content = response["messages"][-1].content

    if isinstance(content, list):
        for item in content:
            if item.get("type") == "text":
                return item["text"]

    return str(content)

def print_final_answer(response):
    content = response["messages"][-1].content

    if isinstance(content, list):
        for item in content:
            if item.get("type") == "text":
                print("\nFinal Answer:")
                print(item["text"])
                return

    print("\nFinal Answer:")
    print(content)

if __name__ == "__main__":
    question = "Show me laptops under $800 with a rating of at least 4."

    response = product_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )

    print_final_answer(response)