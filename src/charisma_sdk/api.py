import requests
from typing import Any, TypedDict, Union, Dict

base_url: str = "https://api.charisma.ai"


class CreatePlaythroughTokenOptionsBase(TypedDict):
    story_id: int


class CreatePlaythroughTokenOptions(CreatePlaythroughTokenOptionsBase, total=False):
    version: int
    api_key: str


def create_playthrough_token(options: CreatePlaythroughTokenOptions) -> str:
    story_id = options["story_id"]
    version = options.get("version")
    api_key = options.get("api_key")

    if version == -1 and api_key is None:
        raise Exception(
            "To play the draft version (-1) of a story, an `api_key` must also be passed."
        )

    headers = {}
    if api_key is not None:
        headers["Authorization"] = f"API-Key {api_key}"

    body = {"storyId": story_id}
    if version is not None:
        body["version"] = version

    response = requests.post(
        f"{base_url}/play/token", json=body, headers=headers, verify=False
    )
    json: Dict[str, Any] = response.json()

    return json["token"]


def create_conversation(token: str) -> int:
    response = requests.post(
        f"{base_url}/play/conversation",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )
    json: Dict[str, Any] = response.json()

    return json["conversationId"]


def set_memory(
    token: str, memory_id_or_recall_value: Union[int, str], save_value: str
) -> None:
    body: Dict[str, Any] = {"saveValue": save_value}
    if memory_id_or_recall_value is int:
        body["memoryId"] = memory_id_or_recall_value
    else:
        body["memoryRecallValue"] = memory_id_or_recall_value

    requests.post(
        f"{base_url}/play/set-memory",
        json=body,
        headers={"Authorization": f"Bearer {token}"},
    )


class MoodModifier(TypedDict, total=False):
    happiness: int
    anger: int
    trust: int
    patience: int
    fearlessness: int


def set_mood(
    token: str, character_id_or_name: Union[int, str], mood_modifier: MoodModifier
):
    body: Dict[str, Any] = {"modifier": mood_modifier}
    if character_id_or_name is int:
        body["characterId"] = character_id_or_name
    else:
        body["characterName"] = character_id_or_name

    response = requests.post(
        f"{base_url}/play/set-mood",
        json=body,
        headers={"Authorization": f"Bearer {token}"},
    )
    json: Dict[str, Any] = response.json()

    return json
