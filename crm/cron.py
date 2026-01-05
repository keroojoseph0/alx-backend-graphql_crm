from datetime import datetime
from gql.transport.requests import RequestsHTTPTransport
from gql import gql ,Client


def log_crm_heartbeat():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    log_message = f"{timestamp} CRM is alive\n"

    # Log heartbeat
    with open("/tmp/crm_heartbeat_log.txt", "a") as file:
        file.write(log_message)

    # OPTIONAL: verify GraphQL endpoint
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.status_code == 200:
            with open("/tmp/crm_heartbeat_log.txt", "a") as file:
                file.write(f"{timestamp} GraphQL endpoint responsive\n")
    except Exception:
        with open("/tmp/crm_heartbeat_log.txt", "a") as file:
            file.write(f"{timestamp} GraphQL endpoint NOT responsive\n")



GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"


def update_low_stock():
    mutation = """
    mutation {
      updateLowStockProducts {
        success
        message
        products {
          name
          stock
        }
      }
    }
    """

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        response = requests.post(
            GRAPHQL_ENDPOINT,
            json={"query": mutation},
            timeout=10
        )
        data = response.json()

        products = data["data"]["updateLowStockProducts"]["products"]

        with open("/tmp/low_stock_updates_log.txt", "a") as file:
            file.write(f"{timestamp} - Low stock update executed\n")
            for product in products:
                file.write(
                    f"{timestamp} - Product: {product['name']}, Stock: {product['stock']}\n"
                )

    except Exception as e:
        with open("/tmp/low_stock_updates_log.txt", "a") as file:
            file.write(f"{timestamp} - ERROR: {str(e)}\n")
