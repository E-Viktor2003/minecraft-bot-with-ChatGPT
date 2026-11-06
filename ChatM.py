import threading

import g4f

from ChatTxt import add_message

# These commands are handled by the bot itself and are never sent to the game chat.
INTERNAL_COMMANDS = ('/memory', '/stop', '/restart')

# Every chat message is processed in its own thread (see Bot.py), so reading and
# writing memory.txt / messages.txt must not happen at the same time.
file_lock = threading.Lock()


def split_text(text, max_length=250):
    text_parts = [text[i:i+max_length] for i in range(0, len(text), max_length)]
    return text_parts


def read_text_file(file_path):
    # memory.txt and messages.txt are created on first use and are not stored
    # in the repository, so they may not exist yet
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return ""


def write_text_file(file_path, text):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(text)


def get_model():
    # g4f.models.gpt_4 exists in older versions of g4f, newer ones use models.default
    return getattr(g4f.models, 'gpt_4', None) or g4f.models.default


def get_provider():
    # the Bing provider is missing in newer versions of g4f; in that case
    # provider=None lets g4f pick any provider that currently works
    try:
        from g4f.Provider import Bing
        return Bing
    except ImportError:
        return None


def memory_lines(memory):
    return [line for line in memory.splitlines() if line.strip()]


def memory_add(memory, text):
    if not text:
        return memory
    lines = memory_lines(memory)
    lines.append(text)
    return "\n".join(lines) + "\n"


def memory_delete(memory, text):
    if not text:
        # an empty "/memory delete" must not wipe the whole memory
        return memory
    lines = memory_lines(memory)
    kept = [line for line in lines if text not in line]
    if len(kept) == len(lines):
        # no whole line matched, fall back to removing the substring
        return memory.replace(text, "")
    return "\n".join(kept) + ("\n" if kept else "")


def memory_replace(memory, text):
    parts = text.split("&")
    if len(parts) < 2:
        return memory
    return memory.replace(parts[0].strip(), parts[1].strip())


def handle_memory_command(part, memory):
    """Applies a /memory command and returns the new content of memory.txt"""
    if 'delete' in part:
        return memory_delete(memory, part.replace('/memory delete', '', 1).strip())
    if 'replace' in part:
        return memory_replace(memory, part.replace('/memory replace', '', 1).strip())
    return memory_add(memory, part.replace('/memory', '', 1).strip())


def send_to_chat(text, bot):
    # the Minecraft chat limit is 256 characters, long answers are split up
    if len(text) < 256:
        bot.chat(text)
    else:
        for part in split_text(text):
            bot.chat(part)
    print("ChatBot: " + text)


def handle_command(part, bot):
    command = part.split()[0].lower()

    if command == '/memory':
        with file_lock:
            memory = read_text_file('memory.txt')
            write_text_file('memory.txt', handle_memory_command(part, memory))
        print("memory updated: " + part)

    elif command == '/stop':
        print("stopping the bot: /stop")
        bot.quit()

    elif command == '/restart':
        print("/restart is not implemented, restart Bot.py manually")

    else:
        # everything else is a Minecraft command: /give, /tp, /gamemode, ...
        bot.chat(part)
        print("command: " + part)


def ChatGPT(Chat, bot):

    promt = read_text_file('promt.txt')

    with file_lock:
        memory = read_text_file('memory.txt')
        messages = read_text_file('messages.txt')

    PromtMemory = promt + "\n information that you have memorized:\n" + memory + "\n past posts:\n" + messages

    try:
        response = g4f.ChatCompletion.create(
            model=get_model(),
            provider=get_provider(),
            messages=[{"role": 'system', "content": PromtMemory}, {"role": "user", "content": Chat}],
            stream=False,
        )
    except Exception as error:
        # a broken provider must not kill the bot, it just skips this message
        print("ChatGPT request failed: " + str(error))
        return

    with file_lock:
        add_message(Chat)

    # the answer is split by "|": before it are Minecraft commands, after it is
    # the text for the chat (see promt.txt)
    for part in response.split("|"):
        part = part.strip()

        if part.startswith("ChatBot:"):
            part = part[len("ChatBot:"):].strip()

        if not part:
            continue

        if part.startswith("/"):
            handle_command(part, bot)
        else:
            send_to_chat(part, bot)
            with file_lock:
                add_message("ChatBot:" + part)
