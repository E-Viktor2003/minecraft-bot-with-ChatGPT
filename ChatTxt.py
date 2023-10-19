
def add_message(message):
    file_path = "messages.txt"
    message = "\n"+message

    try:
        with open(file_path, "r") as file:
            messages = file.readlines()
    except FileNotFoundError:
        messages = []


    messages = messages[-9:]  


    messages.append(message)


    with open(file_path, "w") as file:
        file.writelines(messages)
