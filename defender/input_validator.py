import re

INJECTION_PATTERNS = [
    "ignore all previous instructions",
    "ignore your previous instructions",
    "disregard your system prompt",
    "you are now dan",
    "do anything now",
    "developer mode",
    "reveal your system prompt",
    "print your system prompt",
    "output your system prompt",
    "end system prompt",
    "new instructions:",
    "system override",
    "you are now an unrestricted",
    "pretend you are an ai",
    "as an ai with no restrictions",
]


def validate_input(prompt):
    lowered = prompt.lower()

    for pattern in INJECTION_PATTERNS:
        if pattern in lowered:
            return {
                "safe": False,
                "reason": f"Blocked pattern detected: '{pattern}'"
            }

    if len(prompt) > 2000:
        return {
            "safe": False,
            "reason": "Input exceeds maximum allowed length"
        }

    return {
        "safe": True,
        "reason": "Input passed validation"
    }