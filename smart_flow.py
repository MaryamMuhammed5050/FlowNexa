import re

# ==========================================
# 1. INTENT PARSER & EXTRACTOR (The Smart Router)
# ==========================================
def parse_order_details(trigger_text):
    """
    Analyzes text to see if there is a positive order intent.
    If yes, extracts the quantity and product name automatically.
    """
    trigger_text = trigger_text.lower()

    # 1. First, check if they actually want to buy something (our previous logic)
    positive_intent_pattern = (
        r"\b(want|would like|need|place|make|buy|purchase)\b"
        r"(?:\s+\w+){0,5}\s+\b(order|ordering|buy|buying|purchase|purchasing)\b"
    )
    
    if not re.search(positive_intent_pattern, trigger_text):
        return None # Return None if they aren't trying to buy anything

    # 2. Advanced Extraction Pattern
    # This pattern looks for: Optional text -> A number (\d+) -> Optional space -> An item name (\w+)
    # Example match: "buy 3 shoes" or "order 12 laptops"
    extraction_pattern = r"\b(?:buy|order|purchase|need)\s+(\d+)\s+(\w+)"
    match = re.search(extraction_pattern, trigger_text)

    # Prepare a default dictionary structure to store our extracted data
    extracted_data = {
        "intent": "positive_order",
        "quantity": "1",          # Default to 1 if they didn't specify a number
        "item": "unknown item"    # Default placeholder
    }

    if match:
        # group(1) captures the number, group(2) captures the product word
        extracted_data["quantity"] = match.group(1)
        extracted_data["item"] = match.group(2)
    else:
        # Backup: If they didn't specify a number (e.g., "I want to buy a laptop")
        # We look for a singular item directly after the action verb
        backup_pattern = r"\b(?:buy|order|purchase|need)\s+(?:an?|the)?\s*(\w+)"
        backup_match = re.search(backup_pattern, trigger_text)
        if backup_match:
            extracted_data["item"] = backup_match.group(1)

    return extracted_data


# ==========================================
# 2. AUTOMATION ACTIONS (Dynamic Integrations)
# ==========================================
def execute_smart_order(data):
    """
    Takes the structured dictionary from the parser and saves it.
    Notice we no longer ask the user for a second input()!
    """
    item = data["item"]
    quantity = data["quantity"]

    # Build a clean log string
    log_entry = f"Quantity: {quantity} | Item: {item}"

    with open("order.txt", "a") as file:
        file.write(log_entry + "\n")
        
    print(f"\n[SHOP ACTION EXECUTED]")
    print(f" -> Successfully mapped data to database!")
    print(f" -> Saved Entry: {log_entry}")


# ==========================================
# 3. THE CORE EXECUTION ENGINE (FlowNexa v2)
# ==========================================
print("=== Welcome to FlowNexa v2: Smart Extraction Engine ===")

while True:
    print("\n------------------------------------------------")
    trigger = input("Enter your command (e.g., 'I want to buy 3 laptops'):\n> ")
    
    if trigger.lower() == "exit":
        print("Shutting down FlowNexa. Goodbye!")
        break

    is_request_understood = False

    # Run our new smart extraction parser
    order_data = parse_order_details(trigger)
    
    if order_data is not None:
        # If order_data has content, pass the dictionary right into our action function
        execute_smart_order(order_data)
        is_request_understood = True

    if not is_request_understood:
        print("⚠️ FlowNexa could not extract structured data. Try: 'I want to buy 5 apples'")
