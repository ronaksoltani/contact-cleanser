from __future__ import annotations

import os
import re
from pathlib import Path

import phonenumbers

SAMPLE_DISPOSABLE_DOMAINS = {"mailinator.com", "10minutemail.com", "tempmail.com"}
EMAIL_PATTERN = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def disposable_domains() -> set[str]:
    """Load an optional newline-delimited domain list over the bundled examples."""
    domains = set(SAMPLE_DISPOSABLE_DOMAINS)
    file_name = os.getenv("DISPOSABLE_DOMAINS_FILE")
    if file_name:
        try:
            domains.update(line.strip().lower() for line in Path(file_name).read_text(encoding="utf-8").splitlines()
                           if line.strip() and not line.lstrip().startswith("#"))
        except OSError:
            pass  # A missing optional list should not take down the API.
    return domains


def normalize_email(email: str) -> dict[str, object]:
    value = email.strip()
    valid_syntax = bool(EMAIL_PATTERN.fullmatch(value))
    domain = value.rsplit("@", 1)[-1].lower() if "@" in value else ""
    disposable = domain in disposable_domains()
    return {"valid": valid_syntax and not disposable,
            "normalized": value.lower() if valid_syntax else None,
            "disposable": disposable,
            "reason": "disposable domain" if disposable else (None if valid_syntax else "invalid email syntax")}


def normalize_phone(phone: str, region: str = "US") -> dict[str, object]:
    try:
        parsed = phonenumbers.parse(phone, region.upper())
        valid = phonenumbers.is_valid_number(parsed)
        return {"valid": valid,
                "normalized": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164) if valid else None,
                "reason": None if valid else "not a valid phone number for the selected region"}
    except phonenumbers.NumberParseException as error:
        return {"valid": False, "normalized": None, "reason": str(error)}
