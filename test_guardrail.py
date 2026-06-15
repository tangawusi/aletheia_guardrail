from guardrail import flatten_and_inspect_payload, audit_routing_nodes, process_invoice_stream

def test_fee_detection_loop():
    malicious_payload = [
        [{"id": 101, "fee": 0.0}, {"id": 102, "fee": 0.0}],
        [{"id": 201, "fee": 0.005}, {"id": 202, "fee": 0.0}]
    ]
    _, flagged = flatten_and_inspect_payload(malicious_payload)
    assert flagged is True
    print("Verification Pass: Nested fee inspection loop caught hidden platform taxing.")

def test_gas_exhaustion_bounds():
    # Invoices to process, each consuming 15 units of validation gas
    mock_queue = [
        {"amount": 100.0, "gas_cost": 15},
        {"amount": 250.0, "gas_cost": 15},
        {"amount": 500.0, "gas_cost": 15}
    ]
    # Set gas allowance low so the engine is forced to halt halfway
    count, settled, gas_left = process_invoice_stream(mock_queue, max_gas_allowance=35)
    
    assert count == 2
    assert settled == 350.0
    assert gas_left < 15
    print("Verification Pass: Stream loop terminated perfectly at safe execution limits.")

if __name__ == "__main__":
    test_fee_detection_loop()
    test_gas_exhaustion_bounds()