import re

def wants_order(trigger):
    trigger = trigger.lower()

    negative_order = re.search(
        r"\b(?:don't|do not|didn't|did not|doesn't|does not|"
        r"won't|will not|wouldn't|would not|can't|cannot|"
        r"never|no|not)\b"
        r"(?:\s+\w+){0,6}\s+\b(?:order|ordering)\b",
        trigger
)
if negative_order:
    return False

return "order" in trigger
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
    print(f"your order has been taken: {trigger}")

    with open("order.txt", "a") as file:
        file.write(order + "\n")
        print(f"your order has been saved: {trigger}")



print("Welcome to FlowNexa, a place for easy automations.")

while True:
    trigger = input("what do you want to do?\n")
    if trigger == "exit":
        break
    action_taken = False
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

    if wants_order(trigger):
        create_order(trigger)
        actions.append("order")
        action_taken = True
    # else:
    #     print("kindly make another request")
    if not action_taken:
        print("kindly input a new request")

    print(f"actions detected: {actions}")
