"""Core RSA routines.

This module provides basic RSA operations plus a simple numeric padding scheme.
Cryptanalysis/attacks are intentionally kept out of the package.
"""

from __future__ import annotations

import random
from typing import List, Tuple

import modular


def generate_keys(min_prime: int, max_prime: int) -> Tuple[int, int, int]:
    """Generate RSA keys.

    Returns (n, e, d) where (n, e) is the public key and d is the private exponent.

    Note: this keeps the original lab convention where 'd' is picked first and
    'e' is computed as its modular inverse modulo φ(n).
    """
    primes = modular.list_primes(min_prime, max_prime)
    if len(primes) < 2:
        raise ValueError("prime interval must contain at least two primes")

    p1 = p2 = primes[0]
    attempts = 0
    while p1 == p2:
        p1, p2 = random.choice(primes), random.choice(primes)
        attempts += 1
        if attempts >= 20:
            raise ValueError("interval appears to contain only one prime")

    n = p1 * p2
    phi = (p1 - 1) * (p2 - 1)

    d = 9311
    while not modular.are_coprime(d, phi):
        d += 2

    e = modular.mod_inverse(d, phi)
    if e is None:
        raise ValueError("failed to compute modular inverse for public exponent")

    return int(n), int(e), int(d)


def apply_padding(message_int: int, padding_digits: int) -> int:
    """Append `padding_digits` random decimal digits to message_int."""
    suffix = "".join(str(random.randrange(0, 10)) for _ in range(padding_digits))
    return int(f"{int(message_int)}{suffix}")


def remove_padding(message_int: int, padding_digits: int) -> int:
    """Remove `padding_digits` decimal digits from the end of message_int."""
    text = str(int(message_int))
    if padding_digits <= 0:
        return int(text)
    if len(text) <= padding_digits:
        return 0
    return int(text[: len(text) - padding_digits])


def encrypt_int(message_int: int, n: int, e: int, padding_digits: int) -> int:
    """Encrypt an integer message using RSA with decimal-suffix padding."""
    padded = apply_padding(message_int, padding_digits)
    return modular.mod_pow(padded, e, n)


def decrypt_int(cipher_int: int, n: int, d: int, padding_digits: int) -> int:
    """Decrypt an integer ciphertext produced by :func:`encrypt_int`."""
    padded = modular.mod_pow(cipher_int, d, n)
    return remove_padding(padded, padding_digits)


def encrypt_string(text: str, n: int, e: int, padding_digits: int) -> List[int]:
    """Encrypt a Unicode string character-by-character."""
    return [encrypt_int(ord(ch), n, e, padding_digits) for ch in text]


def decrypt_string(cipher_list: List[int], n: int, d: int, padding_digits: int) -> str:
    """Decrypt a list of integers back into a Unicode string."""
    chars = [chr(decrypt_int(c, n, d, padding_digits)) for c in cipher_list]
    return "".join(chars)
