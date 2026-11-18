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


# Temporary conversation memory.
# We will move this to database.py next.
conversation_history = []


def understand_request(trigger):
    """
    Understands the user's message using Gemini
    and considers previous conversation context.
    """

    history = "\n".join(
        f"{message['role']}: {message['content']}"
        for message in conversation_history[-12:]
    )

    prompt = f"""
You are FlowNexa, an intelligent AI-powered automation assistant.

Your responsibility is to understand users naturally,
recognise their intentions, and help them complete tasks.

You must understand meaning, context, and different ways
people express the same intention.

CONVERSATION HISTORY:
{history}

CURRENT USER MESSAGE:
{trigger}

CLASSIFY THE USER'S INTENTION:

- order: The user clearly wants to purchase or place an order.
- inquiry: The user is asking questions or seeking information.
- email: The user wants to compose, prepare, or send an email.
- workflow: The user wants to create, modify, or manage an automation.
- other: Greetings, casual conversation, unclear messages,
  and requests outside the categories above.

INTELLIGENCE RULES:

1. Understand natural language, including different expressions
   with the same meaning.

2. Use conversation history to understand follow-up messages.

3. Understand references such as "it", "that one", "the first one",
   "how much?", and "go ahead" using previous context.

4. "I need a laptop" is an inquiry, not an order.

5. "I want to order a laptop" is an order.

6. "Can I get a laptop?" is an inquiry unless the context
   clearly establishes an intention to purchase.

7. "How much is a laptop?" is an inquiry.

8. Negative statements must never be treated as orders.

9. Never assume permission to purchase or execute an action.

10. If the user's intention is unclear, ask a clarifying question.

11. Greetings and ordinary conversation are not inquiries.

12. Questions about FlowNexa itself should be answered naturally.

13. Recognise when a user changes their mind or cancels a request.

14. Do not repeat questions when the information is already
    available in the conversation.

15. Extract relevant details from requests, including:
    product, quantity, recipient, purpose, schedule,
    trigger, and other available parameters.

ORDER RULES:

- Set execute_order to true only when the user clearly intends
  to place an order.
- An order must still be confirmed before it is saved.
- Never treat a question about a product as an order.
- If the product is missing, ask the user for it.
- Use quantity 1 when no quantity is specified.

RETURN VALID JSON ONLY:

{{
    "intent": "inquiry",
    "item": null,
    "quantity": 1,
    "execute_order": false,
    "action": "none",
    "reply": "How can I help you?",
    "details": {{}}
}}

The action field must be one of:
- confirm_order
- cancel_order
- create_workflow
- prepare_email
- none

Do not include markdown or explanations outside the JSON.
"""

    response = client.models.generate_content(
        model="gemini-3.5-flash-lite",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            max_output_tokens=600
        )
    )

    result = json.loads(response.text)

    return result


def save_to_file(filename, content):
    """Save a request to its appropriate file."""

    with open(filename, "a", encoding="utf-8") as file:
        file.write(content + "\n")


def remember(role, content):
    """Store a message in temporary conversation memory."""

    conversation_history.append({
        "role": role,
        "content": content
    })


def process_order(result):
    """Prepare an order for user confirmation."""

    item = result.get("item")
    quantity = result.get("quantity", 1)

    if not item:
        print("FlowNexa: What product would you like to order?")
        return None

    try:
        quantity = int(quantity)
    except (ValueError, TypeError):
        quantity = 1

    if quantity < 1:
        quantity = 1

    pending_order = {
        "item": item,
        "quantity": quantity
    }

    print(
        f"\nOrder details: {quantity} x {item}"
    )

    print("Would you like to confirm this order? (yes/no)")

    return pending_order


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

            confirmation = trigger.lower()

            if confirmation in ["yes", "y", "confirm"]:

                save_to_file(
                    "order.txt",
                    f"Quantity: {pending_order['quantity']} | "
                    f"Item: {pending_order['item']}"
                )

                message = (
                    f"Your order for {pending_order['quantity']} "
                    f"x {pending_order['item']} has been saved."
                )

                print("\nFlowNexa:", message)
                remember("assistant", message)

                pending_order = None
                continue

            elif confirmation in ["no", "n", "cancel"]:

                message = "Your order has been cancelled. Nothing was saved."

                print("\nFlowNexa:", message)
                remember("assistant", message)

                pending_order = None
                continue

            else:
                print("Please confirm or cancel your pending order.")
                continue

        remember("user", trigger)

        try:
            result = understand_request(trigger)

        except (json.JSONDecodeError, ValueError, KeyError) as error:
            print("FlowNexa could not understand the response.")
            print("Error:", error)
            continue

        except Exception as error:
            print("FlowNexa could not process that request.")
            print("Error:", error)
            continue

        intent = result.get("intent", "other")
        reply = result.get("reply", "How can I help you?")
        action = result.get("action", "none")

        print("\nFlowNexa:", reply)

        remember("assistant", reply)

        if action == "cancel_order":
            pending_order = None
            print("Pending order cancelled.")
            continue

        if intent == "order":

            if not result.get("execute_order", False):
                continue

            pending_order = process_order(result)

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

            print("FlowNexa is ready to help.")


if __name__ == "__main__":
    main()
