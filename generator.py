"""Core password generation and strength evaluation module.

Uses Python's cryptographically secure secrets module.
"""

from __future__ import annotations

import math
import secrets
import string

DEFAULT_SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?~"
AMBIGUOUS_CHARS = "Il1O0o|`'\";:"


def calculate_entropy(password: str, charset_size: int) -> float:
    """Calculate the information entropy (in bits) of a password given its charset size."""
    if not password or charset_size <= 0:
        return 0.0
    return len(password) * math.log2(charset_size)


def get_strength_assessment(entropy: float) -> tuple[str, str]:
    """Return a human-readable strength description and an ANSI color label.

    Entropy thresholds:
    < 40 bits: Weak
    40 - 59 bits: Moderate
    60 - 79 bits: Strong
    >= 80 bits: Very Strong
    """
    if entropy < 40:
        return "Weak", "red"
    elif entropy < 60:
        return "Moderate", "yellow"
    elif entropy < 80:
        return "Strong", "green"
    else:
        return "Very Strong", "cyan"


def generate_password(
    length: int = 16,
    include_uppercase: bool = True,
    include_lowercase: bool = True,
    include_digits: bool = True,
    include_symbols: bool = True,
    exclude_ambiguous: bool = False,
    custom_symbols: str | None = None,
) -> tuple[str, float, str]:
    """Generate a cryptographically secure random password.

    Args:
        length: Desired length of the password (must be >= 4 if all 4 categories are used).
        include_uppercase: Include A-Z.
        include_lowercase: Include a-z.
        include_digits: Include 0-9.
        include_symbols: Include punctuation/symbols.
        exclude_ambiguous: Exclude characters that look similar (e.g. 1, l, I, 0, O).
        custom_symbols: Optional custom string of symbol characters.

    Returns:
        A tuple of (password, entropy_bits, strength_rating).

    Raises:
        ValueError: If no character sets are selected or length is too short for selected sets.
    """
    if length <= 0:
        raise ValueError("Password length must be a positive integer.")

    symbols = custom_symbols if custom_symbols is not None else DEFAULT_SYMBOLS

    upper = string.ascii_uppercase
    lower = string.ascii_lowercase
    digits = string.digits

    if exclude_ambiguous:
        upper = "".join(c for c in upper if c not in AMBIGUOUS_CHARS)
        lower = "".join(c for c in lower if c not in AMBIGUOUS_CHARS)
        digits = "".join(c for c in digits if c not in AMBIGUOUS_CHARS)
        symbols = "".join(c for c in symbols if c not in AMBIGUOUS_CHARS)

    categories: list[str] = []
    if include_lowercase:
        categories.append(lower)
    if include_uppercase:
        categories.append(upper)
    if include_digits:
        categories.append(digits)
    if include_symbols:
        categories.append(symbols)

    if not categories:
        raise ValueError("At least one character set must be selected.")

    if length < len(categories):
        raise ValueError(
            f"Password length ({length}) is too short to include at least one character "
            f"from each of the {len(categories)} selected character types."
        )

    # Ensure at least one character from each active category
    password_chars = [secrets.choice(cat) for cat in categories]

    # Combine all characters for the remainder of the length
    all_allowed = "".join(categories)
    remaining_length = length - len(password_chars)
    password_chars.extend(secrets.choice(all_allowed) for _ in range(remaining_length))

    # Cryptographically secure shuffle using SystemRandom
    secrets.SystemRandom().shuffle(password_chars)
    password = "".join(password_chars)

    entropy = calculate_entropy(password, len(all_allowed))
    strength, _ = get_strength_assessment(entropy)

    return password, entropy, strength
