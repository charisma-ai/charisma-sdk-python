from charisma_sdk.playthrough import Playthrough
from charisma_sdk.api import (
    create_playthrough_token,
    create_conversation,
    set_memory,
    set_mood,
)

import time


def test_playthrough():
    """Playthrough tests"""
    token = create_playthrough_token({"story_id": 27})
    conversation_id = create_conversation(token)

    set_memory(token, "winston_name_guess", "Bob")
    set_mood(token, "Winston", {"happiness": 15})

    playthrough = Playthrough(token)
    playthrough.on(
        "connection-status",
        lambda new_status: print(f"New connection status: {new_status}"),
    )
    playthrough.on("message", lambda message: print(f"Received a message: {message}"))
    playthrough.connect()

    time.sleep(1)

    playthrough.start({"conversationId": conversation_id})
