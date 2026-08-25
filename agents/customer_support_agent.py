import warnings

warnings.filterwarnings(
    "ignore",
    message="Model 'gemini-3.6-flash' uses fixed sampling defaults*"
)

import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langchain.agents import create_agent

from rag.retriever1 import retrieve_documents
from tools.order_tool import get_order1

load_dotenv()


@tool
def search_company_knowledge(query: str) -> str:
    """Search TechStore company information and policies."""
    documents = retrieve_documents(query)

    if not documents:
        return "No relevant company information was found."

    return "\n\n".join(
        document.page_content
        for document in documents
    )


@tool
def search_order(order_id: str) -> str:
    """Search orders.csv for information about a specific order."""
    order = get_order1(order_id)

    if order is None:
        return f"No order was found with ID {order_id}."

    return str(order)


llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0
)


tools = [
    search_company_knowledge,
    search_order
]


system_prompt = """
You are the TechStore Customer Support Agent.

Your responsibilities are:

- Answer questions about TechStore.
- Answer questions about company policies.
- Handle return, shipping, warranty, and payment questions.
- Handle order status and order information.

Use the search_company_knowledge tool for:
- Company information
- Return policy
- Shipping policy
- Warranty policy
- Payment policy

Use the search_order tool for:
- Order status
- Order information
- Delivery information

Never invent company policies or order information.

If the customer asks about an order but does not provide an order ID,
ask the customer for their order ID.

Give clear and helpful answers based on the information returned by
the available tools.
"""


customer_support_agent = create_agent(
    model=llm,
    tools=tools,
    system_prompt=system_prompt
)

def get_answer(response):
    content = response["messages"][-1].content

    if isinstance(content, list):
        for item in content:
            if item.get("type") == "text":
                return item["text"]

    return str(content)

def ask_customer_support(question: str) -> str:
    response = customer_support_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ]
        }
    )

    return get_answer(response)
if __name__ == "__main__":
    question = "What is the status of my order?"

    answer = ask_customer_support(question)

    print("\nFinal Answer:")
    print(answer)