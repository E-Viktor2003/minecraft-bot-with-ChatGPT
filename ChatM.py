from javascript import require,On,Once,AsyncTask,once

import g4f,threading
from ChatTxt import add_message

from g4f.Provider import (
    Bard,
    Bing,
    HuggingChat,
    OpenAssistant,
    OpenaiChat,
    Liaobots,
    Phind,
    Raycast,
    GeekGpt,
)

def split_text(text, max_length=250):
    text_parts = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    return text_parts

def ChatGPT(Chat,bot):

    with open('promt.txt', 'r') as file:
        promt = file.read()

    with open('memory.txt', 'r') as file:
        memory = file.read()

    with open('messages.txt', 'r') as file:
        messages = file.read()

    PromtMemory = promt +"\n информация которое ты запомнил:\n" + memory +"\n прошлые собшения:\n"+messages 

    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        provider=Bing,
        messages=[{"role":'system',"content": PromtMemory },{"role": "user", "content": Chat}],
        stream=False,

    )




    Bot_Replied =   response.replace(" /", "/").split("|")
    add_message(Chat)
    for Bot_Replied1 in Bot_Replied:

        if Bot_Replied1.startswith("ChatBot:"):
            Bot_Replied1 = Bot_Replied1[len("ChatBot:"):]


        if not Bot_Replied1.startswith("/"):
             add_message("ChatBot:"+Bot_Replied1)
        if "/memory" in Bot_Replied1:
            print(Bot_Replied1)
            if "delete" in Bot_Replied1:
                print("-----")
                Bot_Replied12 = Bot_Replied1.replace("/memory delete", '')
                memory2 = memory.replace(Bot_Replied12, "")
                print(memory2+"123")
                with open('memory.txt', 'w') as file:
                    file.write(memory2)

            elif "replace" in Bot_Replied1:
                Bot_Replied12 = Bot_Replied1.replace("/memory replace", '')
                memory2 = Bot_Replied12.split("&")
                print(memory2)
                memory3 = memory.replace(memory2[0],memory2[1])

                with open('memory.txt', 'w') as file:
                    file.write(memory3)

            else:
                Bot_Replied12 = Bot_Replied1.replace("/memory", '')
                with open('memory.txt', 'a') as file:
                    file.write("\n"+Bot_Replied12)
        if len(Bot_Replied1) < 256:
          if not "/stop" in Bot_Replied1 or "/restart" in Bot_Replied1 or "/memory" in Bot_Replied1:
              bot.chat(Bot_Replied1)
        else:
          Bot_Replied1 = split_text(Bot_Replied1)
          for Replied in Bot_Replied1:
            if not Replied.startswith("/"):
              bot.chat(Replied)

        print(Bot_Replied1)

