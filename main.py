import re

def get_order_intent(trigger):
    trigger = trigger.lower()

    negative_order = re.search(
        r"\b(?:don't|dont|do not|didn't|didnt|did not|"
        r"doesn't|doesnt|does not|won't|wont|will not|"
        r"wouldn't|wouldnt|would not|can't|cant|cannot|"
        r"never|no|not)\b"
        r"(?:\s+\w+){0,6}\s+\b(?:order|ordering|buy|buying|"
        r"purchase|purchasing)\b",
        trigger
    )

    if negative_order:
        return "negative"

    positive_order = re.search(
        r"\b(?:want|wants|would like|need|needs|place|placing|"
        r"make|making|buy|buying|purchase|purchasing)\b"
        r"(?:\s+\w+){0,5}\s+\b(?:order|ordering|buy|buying|"
        r"purchase|purchasing)\b",
        trigger
    )

    if positive_order:
        return "positive"

    return "unknown"

def save_request(trigger):

    with open("request.txt", "a") as file:
        file.write(trigger + "\n")
        print(f"your request has been saved: {trigger}")

def send_email(trigger):
    print(f"a confirmation email has been sent to you: {trigger}")

    with open("email.txt", "a") as file:
        file.write(trigger + "\n")
        print(f"your email has been saved: {trigger}")

 
def create_order(trigger):
    order = input("what would you like to order?\n")
    # print(f"your order has been taken: {trigger}")

    order = re.sub(
        r"^(?:i\s+)?(?:want\s+to\s+|would\s+like\s+to\s+|need\s+to\s+|"
        r"would\s+like\s+|want\s+|need\s+|place\s+|placing\s+|"
        r"make\s+|making\s+|buy\s+|buying\s+|purchase\s+|purchasing\s+)?"
        r"(?:an?\s+)?order\s+",
        "",
        order,
        flags=re.IGNORECASE
    )

    with open("order.txt", "a") as file:
        file.write(order + "\n")

        # print(f"your order has been taken: {order}")
        print(f"your order has been saved: {order}")
def is_negative_order(trigger):



    print("Welcome to FlowNexa, a place for easy automations.")

while True:
    trigger = input("what do you want to do?\n")
    if trigger.lower() == "exit":
        break
    action_taken = False
    request_understood = False
    actions = []

     

    if "workflow" in trigger:
        save_request(trigger)
        actions.append("workflow")
        print(f"Your request has been received, workflow started: {trigger}")
        action_taken = True

    if "email" in trigger:
        send_email(trigger)
        actions.append("email")
        action_taken = True

    order_intent = get_order_intent(trigger)

    if order_intent == "positive":
        create_order()
        actions.append("order")
        action_taken = True
        request_understood = True

    elif order_intent == "negative":
        print("Okay, no order will be placed.")
        request_understood = True
    # else:
    #     print("kindly make another request")
if not request_understood:
    print("kindly input a new request.")

    print(f"Actions detected: {actions}")
