import warnings

warnings.filterwarnings(
    "ignore",
    message="Model 'gemini-3.6-flash' uses fixed sampling defaults*"
)

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_agent

from agents.customer_support_agent import ask_customer_support
from agents.product_agent import get_product_answer


load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)


@tool
def customer_support_tool(question: str) -> str:
    """Handle company, policy, shipping, payment, warranty, return, and order questions."""

    return ask_customer_support(question)


@tool
def product_tool(question: str) -> str:
    """Handle product search, product details, specifications, prices, and recommendations."""

    return get_product_answer(question)


tools = [
    customer_support_tool,
    product_tool
]


system_prompt = """
You are the TechStore Routing Agent.

Your job is to understand the customer's question and automatically
send it to the correct specialized agent.

There are two specialized agents:

1. Customer Support Agent
- Company information
- Return policy
- Shipping policy
- Warranty policy
- Payment policy
- Order status
- Order information

2. Product Agent
- Available products
- Product details
- Product specifications
- Product prices
- Product stock
- Product recommendations

Use the customer_support_tool for customer support and order questions.

Use the product_tool for product-related questions.

Always route the customer's question to the appropriate agent.
Do not answer the customer's question yourself.
"""


routing_agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)


def ask_routing_agent(question: str) -> str:

    response = routing_agent.invoke(
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


if __name__ == "__main__":

    question = "What laptops do you have under $700?"

    answer = ask_routing_agent(question)

    print("\nFinal Answer:")
    print(answer)