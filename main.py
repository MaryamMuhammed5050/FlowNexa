def save_request(trigger):

    with open("request.txt", "a") as file:
        file.write(trigger + "\n")
        print(f"your request has been saved: {trigger}")

# print("Welcome to FlowNexa, a place for easy automations.")

# while True:
#     trigger = input("what do you want to do?\n")
#     if trigger == "exit":
#         break
#     if "workflow" in trigger:
#         print(f"Your request has been received, workflow started: {trigger}")


#     elif "email" in trigger:
#         print(f"email action has been selected: {trigger}")
#     else:
#         print("kindly make another request")


def create_order(trigger):
    print("input your order")

def send_email(trigger):
    print("email action")
