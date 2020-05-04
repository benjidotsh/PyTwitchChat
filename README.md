# PyTwitchChat

PyTwitchChat is a Python package to interact with the chat of a Twitch channel.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install PyTwitchChat.

```bash
pip install pytwitchchat
```

## Usage

```python
from pytwitchchat import TwitchChatClient

TWITCH_CHAT_CLIENT = TwitchChatClient(password, username, channel, handler)
TWITCH_CHAT_CLIENT.connect()
TWITCH_CHAT_CLIENT.run()

def handle(message, user, is_mod):
    print(user + " says " + message + " and " + "is a moderator." if is_mod else "is not a moderator.")
```

* **\<password>** needs to be an OAuth token. You can use [Twitch Chat OAuth Password Generator](https://twitchapps.com/tmi) to generate an OAauth token.
* **\<username>** and **\<channel>** need to be in lowercase.
* **handler** is not required.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)