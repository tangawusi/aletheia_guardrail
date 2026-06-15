def flatten_and_inspect_payload(payload_matrix):
    """
    Unpacks a 2D matrix of invoice items into a flat list and flags 
    any items containing an unauthorized platform fee.
    """
    clean_items = []
    has_unauthorized_fees = False
    
    for batch in payload_matrix:
        for item in batch:
            if item["fee"] > 0:
                has_unauthorized_fees = True

            clean_items.append(item)

    return clean_items, has_unauthorized_fees

def audit_routing_nodes(transaction_hop_matrix, blacklist):
    flagged_pipelines = []

    for index, route in enumerate(transaction_hop_matrix):
        for address in route:
            if address in blacklist:
                flagged_pipelines.append(index)
    
    return flagged_pipelines

def process_invoice_stream(invoice_que, max_gas_allowance):
    processed_count = 0
    total_settled_value = 0.0
    remaining_gas = max_gas_allowance

    while len(invoice_que) > 0 and remaining_gas >= 10:
        current_invoice = invoice_que.pop(0)
        remaining_gas = remaining_gas - current_invoice["gas_cost"]
        total_settled_value = total_settled_value + current_invoice["amount"]
        processed_count = processed_count + 1

    return processed_count, total_settled_value, remaining_gas
