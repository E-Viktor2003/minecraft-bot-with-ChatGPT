# Minecraft bot with ChatGPT

[Русский](README_RU.md) | **English**

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)
![Node.js](https://img.shields.io/badge/Node.js-18%2B-green.svg)

A Minecraft bot with ChatGPT can execute Minecraft commands, remember certain information, and remember previous dialog.

## How it works

1. `Bot.py` connects to the server through [Mineflayer](https://github.com/PrismarineJS/mineflayer) (a Node.js library that is launched from Python via the `javascript` package) and listens to the chat.
2. Every message is sent to `ChatM.py`, which builds a request to ChatGPT (the `g4f` library): the prompt from `promt.txt`, the bot's memory (`memory.txt`) and the last messages (`messages.txt`).
3. The model replies in the format `/command | text`. The bot executes everything before `|` as a Minecraft command (it needs operator rights) and writes everything after `|` into the chat. Long answers are split into parts of 250 characters.
4. The `/memory` command lets the bot store, replace and delete information between restarts.

## Requirements

- [Python 3.10 or newer](https://www.python.org/)
- [Node.js 18 or newer](https://nodejs.org/)
- A Minecraft server where the bot has **operator rights** (otherwise it will not be able to execute commands)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/E-Viktor2003/minecraft-bot-with-ChatGPT.git
   cd minecraft-bot-with-ChatGPT
   ```
2. Install the Python dependencies (`javascript`, `g4f`):
   ```bash
   pip install -r requirements.txt
   ```
3. Install the Node.js dependency (`mineflayer`):
   ```bash
   npm install
   ```

## Configuration and launch

1. Open `config.py` and change the values as needed:

   | Parameter | Description |
   | --- | --- |
   | `minecraft_version` | Minecraft server version, e.g. `1.16.5` |
   | `host` | server address (`localhost` for a local server) |
   | `port` | server port; if there is no port, use `25565` |
   | `username` | the bot's nickname |

2. Run the bot:
   ```bash
   python Bot.py
   ```
3. Wait for the bot to join the server. After it has joined, type any message in the chat and wait for a response.

## Project structure

```
Bot.py          - entry point: connects to the server and listens to the chat
ChatM.py        - request to ChatGPT, handling of commands and /memory
ChatTxt.py      - storage of the last 10 chat messages
config.py       - server connection settings
promt.txt       - the system prompt that describes the bot's behaviour
memory.txt      - the bot's long-term memory (created automatically, not stored in git)
messages.txt    - recent dialogue history (created automatically, not stored in git)
requirements.txt - Python dependencies
package.json    - Node.js dependencies
```

## Notes

- `memory.txt` and `messages.txt` are runtime data: they are created automatically and are listed in `.gitignore`, so your dialogue history will not be committed to the repository.
- The `g4f` library uses public providers, which change and break often. If the bot stops answering, update the library (`pip install -U g4f`) and, if necessary, change the provider in `ChatM.py`.
- The message `the bot successfully logged into the server` is printed as soon as the connection is established; the first answer from the model can take a few seconds.

## License

[MIT](LICENSE)
