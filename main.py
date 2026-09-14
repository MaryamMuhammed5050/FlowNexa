def save_request(trigger):

    with open("request.txt", "a") as file:
        file.write(trigger + "\n")
        print(f"your request has been saved: {trigger}")

def send_email(trigger):
    print(f"a confirmation email has been sent to you: {order}")


def create_order(trigger):
    order = input("what would you like to order?\n")
    print(f"your order has been taken: {order}")

    with open("order.txt", "a") as file:
        file.write(order + "\n")
        print(f"your order has been saved: {order}")



print("Welcome to FlowNexa, a place for easy automations.")

while True:
    trigger = input("what do you want to do?\n")
    if trigger == "exit":
        break
    if "workflow" in trigger:
        print(f"Your request has been received, workflow started: {trigger}")


    elif "email" in trigger:
        send_email(trigger)

    elif "order" in trigger:
        create_order(trigger)
    else:
        print("kindly make another request")


