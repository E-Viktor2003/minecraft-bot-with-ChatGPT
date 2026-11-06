
def add_message(message):
    file_path = "messages.txt"
    message = "\n"+message

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            messages = file.readlines()
    except FileNotFoundError:
        messages = []


    messages = messages[-9:]  


    messages.append(message)


    with open(file_path, "w", encoding="utf-8") as file:
        file.writelines(messages)
