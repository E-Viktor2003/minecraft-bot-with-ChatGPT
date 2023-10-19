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



@On(bot,'chat')
def msgHandler(this,user,message,*args):
    if not user == "ChatBot":
        if not "Set own game mode to" in message:
            print(user+":"+message)

            background_thread = threading.Thread(target=ChatGPT, args=(user+":"+message,bot))
            background_thread.start()

while True:  
    pass
