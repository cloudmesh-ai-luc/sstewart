
"""Local AI-assisted emergency message triage."""

import httpx

from pydantic import BaseModel, Field
from typing import Literal

from app.services.config import get_ollama_config


class TriageResult(BaseModel):
    """Validated AI-generated triage suggestion."""

    suggested_priority: Literal[
        "UNCLASSIFIED",
        "LOW",
        "MODERATE",
        "HIGH",
        "CRITICAL",
    ]

    suggested_category: Literal[
        "MEDICAL",
        "FIRE",
        "CRIME",
        "ACCIDENT",
        "HAZARD",
        "OTHER",
        "UNKNOWN",
    ]

    explanation: str = Field(min_length=1, max_length=500)

    confidence: float = Field(ge=0.0, le=1.0)


class OllamaUnavailableError(Exception):
    """Raised when Ollama cannot be reached."""


class OllamaResponseError(Exception):
    """Raised when Ollama returns an invalid response."""


SYSTEM_PROMPT = """
You are an AI assistant for an educational, synthetic
emergency-message analysis application.

Your task is to analyze a synthetic emergency message
and suggest a category and priority.

Available priorities:
- UNCLASSIFIED
- LOW
- MODERATE
- HIGH
- CRITICAL

Available categories:
- MEDICAL
- FIRE
- CRIME
- ACCIDENT
- HAZARD
- OTHER
- UNKNOWN

Guidelines:

1. Only use information explicitly provided in the message.
2. Do not invent details or assume facts that are not present.
3. Use UNCLASSIFIED when there is insufficient information
   to suggest a priority.
4. Use UNKNOWN when the category cannot be determined.
5. Explain the reasoning briefly and objectively.
6. Confidence must be a number between 0.0 and 1.0.
7. Confidence is an approximate model self-assessment,
   not a statistically calibrated probability.
8. Never claim that emergency services have been contacted.
9. Never provide instructions for dispatching responders.
10. Return only the structured JSON requested.

Your output is a suggestion for a human operator.
A human operator always makes the final decision.
"""


def analyze_message(message_text: str) -> TriageResult:
    """Analyze a synthetic emergency message using Ollama."""

    if not message_text or not message_text.strip():
        raise ValueError("Message text cannot be empty.")

    config = get_ollama_config()

    request_payload = {
        "model": config["model"],
        "stream": False,
        "format": TriageResult.model_json_schema(),
        "options": {
            "temperature": 0,
        },
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": (
                    "Analyze this synthetic emergency message:\n\n"
                    f"{message_text}"
                ),
            },
        ],
    }

    try:
        with httpx.Client(timeout=config["timeout"]) as client:
            response = client.post(
                f"{config['base_url']}/api/chat",
                json=request_payload,
            )

            response.raise_for_status()

    except httpx.HTTPError as exc:
        raise OllamaUnavailableError(
            "Unable to communicate with the Ollama service."
        ) from exc

    try:
        response_data = response.json()
        generated_content = response_data["message"]["content"]

        result = TriageResult.model_validate_json(
            generated_content
        )

        return result

    except (ValueError, KeyError, TypeError) as exc:
        raise OllamaResponseError(
            "Ollama returned an invalid triage response."
        ) from exc
