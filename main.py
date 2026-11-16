# import re


# def get_order_intent(trigger):
#     trigger = trigger.lower()

#     negative_order = re.search(
#         r"\b(?:don't|dont|do not|didn't|didnt|did not|"
#         r"doesn't|doesnt|does not|won't|wont|will not|"
#         r"wouldn't|wouldnt|would not|can't|cant|cannot|"
#         r"never|no|not)\b"
#         r"(?:\s+\w+){0,6}\s+\b(?:order|ordering|buy|buying|"
#         r"purchase|purchasing)\b",
#         trigger
#     )

#     if negative_order:
#         return "negative"

#     positive_order = re.search(
#         r"\b(?:want|wants|would like|need|needs|plan to|"
#         r"place|placing|make|making)\b"
#         r"(?:\s+\w+){0,5}\s+\b(?:order|ordering|buy|buying|"
#         r"purchase|purchasing)\b"
#         r"|\b(?:buy|purchase|order)\b",
#         trigger
#     )

#     if positive_order:
#         return "positive"

#     return "unknown"


# def save_request(trigger):
#     with open("request.txt", "a") as file:
#         file.write(trigger + "\n")

#     print(f"Your request has been saved: {trigger}")


# def send_email(trigger):
#     with open("email.txt", "a") as file:
#         file.write(trigger + "\n")

#     print(f"Your email request has been recorded: {trigger}")


# def create_order(trigger):
#     print(f"Order request: {trigger}")

#     while True:
#         order = input("What would you like to order?\n").strip()

#         if order:
#             break

#         print("Please enter an item.")

#     with open("order.txt", "a") as file:
#         file.write(order + "\n")

#     print(f"Your order has been saved: {order}")


# def main():
#     print("Welcome to FlowNexa, a place for easy automations.")

#     while True:
#         trigger = input("\nWhat do you want to do?\n").strip()

#         if trigger.lower() == "exit":
#             print("Thank you for using FlowNexa. Goodbye!")
#             break

#         request_understood = False
#         actions = []

#         if "workflow" in trigger.lower():
#             save_request(trigger)
#             actions.append("workflow")
#             print(f"Your workflow request has been received: {trigger}")
#             request_understood = True

#         if "email" in trigger.lower():
#             send_email(trigger)
#             actions.append("email")
#             request_understood = True

#         order_intent = get_order_intent(trigger)

#         if order_intent == "positive":
#             create_order(trigger)
#             actions.append("order")
#             request_understood = True

#         elif order_intent == "negative":
#             print("Okay, no order will be placed.")
#             request_understood = True

#         if not request_understood:
#             print("Kindly enter a new request.")

#         if actions:
#             print(f"Actions detected: {actions}")


# if __name__ == "__main__":
#     main()



import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise SystemExit("Gemini API key not found. Check your .env file.")

client = genai.Client(api_key=api_key)


def understand_request(trigger):
    prompt = f"""
Analyse this user request for FlowNexa, an automation platform.

Choose one intent:
- order: The user clearly wants to buy something.
- inquiry: The user is asking a question or expressing interest.
- email: The user wants to send or prepare an email.
- workflow: The user wants to create an automation.
- other: Anything else.

Rules:
- "I need a laptop" is an inquiry, not an order.
- "I want to order a laptop" is an order.
- "I want to compare laptop prices" is an inquiry.
- Negative statements must not be treated as orders.
- Never interpret an unclear message as permission to order.
- Extract the product name and quantity when available.
- Use quantity 1 if it is not specified.
- Set execute_order to true only for a clear order request.

Return JSON only, using this structure:
{{
    "intent": "order",
    "item": "laptop",
    "quantity": 1,
    "execute_order": true,
    "reply": "Your order request has been understood."
}}

User message: {trigger}
"""

    response = client.models.generate_content(
      model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            max_output_tokens=300
        )
    )

    return json.loads(response.text)


def save_to_file(filename, content):
    with open(filename, "a") as file:
        file.write(content + "\n")


def main():
    print("Welcome to FlowNexa, a place for easy automations.")

    pending_order = None

    while True:
        trigger = input("\nWhat do you want to do?\n").strip()

        if not trigger:
            print("Please enter a request.")
            continue

        if trigger.lower() == "exit":
            print("Thank you for using FlowNexa. Goodbye!")
            break

        if pending_order:
            if trigger.lower() in ["yes", "y", "confirm"]:
                save_to_file(
                    "order.txt",
                    f"Quantity: {pending_order['quantity']} | "
                    f"Item: {pending_order['item']}"
                )
                print("Your order has been saved successfully!")
                pending_order = None
                continue

            elif trigger.lower() in ["no", "n", "cancel"]:
                print("Order cancelled. Nothing was saved.")
                pending_order = None
                continue

            else:
                print("Please confirm your pending order with yes or no.")
                continue

        try:
            result = understand_request(trigger)

        except Exception as error:
            print("FlowNexa could not process that request.")
            print("Error:", error)
            continue

        intent = result.get("intent", "other")
        reply = result.get("reply", "How can I help you?")

        print("\nFlowNexa:", reply)

        if intent == "order":
            if not result.get("execute_order", False):
                print("Please clarify whether you want to place an order.")
                continue

            item = result.get("item")

            if not item or item == "unknown":
                print("What product would you like to order?")
                continue

            pending_order = {
                "item": item,
                "quantity": result.get("quantity", 1)
            }

            print(
                f"Order details: {pending_order['quantity']} "
                f"x {pending_order['item']}"
            )
            print("Would you like to confirm this order? (yes/no)")

        elif intent == "email":
            save_to_file("email.txt", trigger)
            print("Email request recorded.")
            print("Actions detected: ['email']")

        elif intent == "workflow":
            save_to_file("request.txt", trigger)
            print("Workflow request saved.")
            print("Actions detected: ['workflow']")

        elif intent == "inquiry":
            save_to_file("request.txt", trigger)
            print("Inquiry recorded.")
            print("Actions detected: ['inquiry']")

        else:
            print("I'm ready to help. Tell me what you'd like to do.")


if __name__ == "__main__":
    main()