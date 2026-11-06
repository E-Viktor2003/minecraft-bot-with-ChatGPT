from javascript import require,On,once
from ChatM import ChatGPT

import threading
import config

mineflayer = require('mineflayer')

bot = mineflayer.createBot({
    'host': config.host,
    'port': config.port,
    'version': config.minecraft_version,
    'username': config.username 
})


once(bot, 'login')
bot.chat('hi')
print("the bot successfully logged into the server")

# is set when the connection to the server is closed (for example by /stop)
stop_event = threading.Event()


@On(bot,'chat')
def msgHandler(this,user,message,*args):
    # the bot must not answer its own messages, otherwise it loops forever
    if not user == config.username:
        if not "Set own game mode to" in message:
            print(user+":"+message)

            background_thread = threading.Thread(target=ChatGPT, args=(user+":"+message,bot), daemon=True)
            background_thread.start()


@On(bot,'end')
def endHandler(*args):
    print("connection to the server closed")
    stop_event.set()


while not stop_event.wait(0.5):
    pass
