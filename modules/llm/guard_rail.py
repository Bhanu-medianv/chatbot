import re


INJECTION_PATTERNS = [
    r"ignore (all |the )?(previous|prior|above) (instructions?|prompts?|rules?)",
    r"disregard (the |all )?(previous|prior|earlier)",
    r"forget (everything|your instructions?|the rules?)",
    r"you are (now |a )?(DAN|jailbroken|unrestricted|unfiltered)",
    r"pretend (you are|to be) .{0,40}(no restrictions?|uncensored)",
    r"</?(system|user|assistant|im_start|im_end)>",
    r"new (instructions?|system prompt|rules?):",
    r"reveal your (system )?prompt",
    r"what (are|were) your (original )?instructions?",
]


def is_prompt_injection(user_message: str) -> bool:
    """
    Check for common prompt injection patterns.
    """

    for pattern in INJECTION_PATTERNS:
        if re.search(
            pattern,
            user_message,
            re.IGNORECASE,
        ):
            return True

    return False


def check_guardrail(user_message: str) -> bool:
    """
    Rule-based injection check only.

    Scope enforcement (dental-clinic-only topics) is now handled
    directly by the main LLM via its system prompt, avoiding a
    second Groq round-trip per turn.
    """

    if is_prompt_injection(user_message):
        print("[guardrail] prompt injection detected")
        return False

    return True