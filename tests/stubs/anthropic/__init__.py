"""Offline stand-in for the ``anthropic`` package, used only by the smoke tests.

It records each ``messages.create`` call and returns a fixed text response, so the
tutorial notebooks can be executed end to end without an API key or network access.
It does not reproduce the real SDK's behaviour beyond the attributes the notebooks use.
"""

from types import SimpleNamespace

STUB_TEXT = "This is a stubbed response from the offline test double."
calls = []


class _Messages:
    def create(self, **kwargs):
        if not kwargs.get("model"):
            raise ValueError("model is required")
        for message in kwargs.get("messages", []):
            if not isinstance(message, dict):
                # The real SDK fails here too; the tutorial shows this on purpose.
                raise TypeError(f"Object of type {type(message).__name__} is not JSON serializable")
        calls.append(kwargs)
        return SimpleNamespace(
            content=[SimpleNamespace(type="text", text=STUB_TEXT)],
            stop_reason="end_turn",
            model=kwargs["model"],
        )


class Anthropic:
    def __init__(self, api_key=None, **kwargs):
        self.api_key = api_key
        self.messages = _Messages()


AnthropicBedrock = Anthropic
