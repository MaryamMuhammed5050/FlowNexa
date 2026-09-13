print("Welcome to FlowNexa, a place for easy automations.")
trigger = input("what do you want to do?\n")

if trigger == "start a workflow":
    print(f"Your request has been received, workflow started: {trigger}")
else:
    print("kindly make another request")

    with open("request.txt", "a") as file:
        file.write(trigger + "\n")

    print(f"your request has been saved: {trigger}")
