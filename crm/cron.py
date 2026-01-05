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


