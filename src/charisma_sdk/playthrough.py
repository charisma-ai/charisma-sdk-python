import socketio  # type: ignore
from pyee import EventEmitter  # type: ignore
from typing import Any, Optional, TypedDict

from .api import base_url


class SpeechConfig(TypedDict):
    encoding: str
    output: str


class StartEvent(TypedDict):
    conversationId: int


class ReplyEvent(TypedDict):
    conversationId: int
    text: str


class TapEvent(TypedDict):
    conversationId: int


class ResumeEvent(TypedDict):
    conversationId: int


class Playthrough(EventEmitter):
    token: str

    connection_status: str

    speech_config: Optional[SpeechConfig]

    def __init__(self, token: str, speech_config: SpeechConfig = None) -> None:
        super().__init__()

        self.token = token
        self.connection_status = "disconnected"
        self.speech_config = speech_config

    def connect(self) -> None:
        self.socket = socketio.Client()

        self.socket.connect(
            base_url + "/?token=" + self.token,
            transports=["websocket"],
            namespaces=["/play"],
        )

        # Fired upon a successful reconnection.
        self.socket.on("reconnect", self.on_reconnect, "/play")
        # Fired upon an attempt to reconnect.
        self.socket.on("reconnecting", self.on_reconnecting, "/play")
        # Fired upon a disconnection.
        self.socket.on("disconnect", self.on_disconnect, "/play")
        # Fired when an error occurs.
        self.socket.on("error", self.on_error, "/play")

        self.socket.on("status", self.on_status, "/play")
        self.socket.on("problem", self.on_problem, "/play")
        self.socket.on("start-typing", self.on_start_typing, "/play")
        self.socket.on("stop-typing", self.on_stop_typing, "/play")
        self.socket.on("message", self.on_message, "/play")
        self.socket.on("episode-complete", self.on_episode_complete, "/play")

    def disconnect(self) -> None:
        if self.socket:
            self.socket.disconnect()
            self.socket = None

    def change_connection_status(self, new_connection_status) -> None:
        if new_connection_status != self.connection_status:
            self.connection_status = new_connection_status
            self.emit("connection-status", new_connection_status)

    def on_reconnect(self) -> None:
        pass

    def on_reconnecting(self) -> None:
        self.change_connection_status("reconnecting")

    def on_disconnect(self) -> None:
        self.change_connection_status("disconnected")

    def on_status(self, status) -> None:
        self.change_connection_status("connected")

    def on_error(self, error) -> None:
        self.emit("error", error)

    def on_problem(self, problem) -> None:
        self.emit("problem", problem)

    def on_start_typing(self, event) -> None:
        self.emit("start-typing", event)

    def on_stop_typing(self, event) -> None:
        self.emit("stop-typing", event)

    def on_message(self, event) -> None:
        self.emit("message", event)

    def on_episode_complete(self, event) -> None:
        self.emit("episode-complete", event)

    def add_outgoing_event(self, event_name: str, event_data: Any) -> None:
        if self.socket:
            if self.connection_status == "connected":
                self.socket.emit(event_name, event_data, "/play")
            else:
                print(
                    f"Event `{event_name}` was not sent as the socket was not ready. Wait for the `connection-status` event to be called with `connected` before sending events."
                )
        else:
            print(
                f"Event `{event_name}` was not sent as the socket was not initialised. Call `playthrough.connect()` to connect the socket."
            )

    def start(self, event: StartEvent) -> None:
        self.add_outgoing_event("start", event)

    def reply(self, event: ReplyEvent) -> None:
        self.add_outgoing_event("reply", event)

    def tap(self, event: TapEvent) -> None:
        self.add_outgoing_event("tap", event)

    def resume(self, event: ResumeEvent) -> None:
        self.add_outgoing_event("resume", event)
