# Charisma.ai SDK for Python

```bash
pip install charisma-sdk
```


## Usage

```python
from charisma_sdk.playthrough import Playthrough
from charisma_sdk.api import (
    create_playthrough_token,
    create_conversation,
    set_memory,
    set_mood,
)

story_id = 1

token = create_playthrough_token({"story_id": story_id})
conversation_id = create_conversation(token)

set_memory(token, "my_memory_recall", "the value to save!")
set_mood(token, "My Character Name", {"happiness": 15})

playthrough = Playthrough(token)
playthrough.on("message", lambda message: print("Received a message:", message))
playthrough.connect()

# Some time later...
playthrough.start({"conversationId": conversation_id})
# Some time later...
playthrough.reply({"conversationId": conversation_id, "text": "This is my message to send to Charisma."})
```

## Questions?

Get in touch with us at ben@charisma.ai and we'll be happy to help you out!
