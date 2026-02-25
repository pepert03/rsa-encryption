"""RSA attack helpers (kept outside packages).

This file intentionally lives at the project root, as requested.
"""

from __future__ import annotations

from typing import Dict, List

import modular


def recover_private_exponent(n: int, e: int) -> int:
    """Recover d from public key (n, e) by factoring n.

    This is only feasible for small n in practice.
    """
    factors = modular.factorize(n)
    if len(factors) == 0:
        raise ValueError("n must be > 1")

    p1 = next(iter(factors.keys()))
    p2 = n // p1
    phi = (p1 - 1) * (p2 - 1)

    d = modular.mod_inverse(e, phi)
    if d is None:
        raise ValueError("e has no inverse modulo phi")
    return int(d)


def known_plaintext_dictionary_attack(cipher_list: List[int], n: int, e: int) -> str:
    """Decrypt by building a dictionary of all Unicode codepoints.

    Works only if the plaintext is encrypted per-character without padding.
    """
    table: Dict[int, str] = {}
    for codepoint in range(65536):
        table[modular.mod_pow(codepoint, e, n)] = chr(codepoint)

    return "".join(table[c] for c in cipher_list)


def padding_bruteforce_attack(
    cipher_list: List[int],
    n: int,
    e: int,
    padding_digits: int,
) -> str:
    """Bruteforce the decimal-suffix padding given a likely character set."""
    characters = (
        " eaosrnidlctumpbgvEAOSRNIDLCTUMPGBV"
        "áéíóú.,yqhfzjñxkwYQHFZJÑXKWÁÉÍÓÚ0123456789"
    )

    recovered: List[str] = ["-"] * len(cipher_list)
    found = 0

    for ch in characters:
        start = int(f"{ord(ch)}{'0' * padding_digits}")
        end = start + int("9" * padding_digits)

        for guess in range(start, end + 1):
            candidate = modular.mod_pow(guess, e, n)
            if candidate in cipher_list:
                idx = cipher_list.index(candidate)
                if recovered[idx] == "-":
                    recovered[idx] = ch
                    found += 1
                    if found == len(cipher_list):
                        return "".join(recovered)
                message = "".join(recovered)
                print(message)

        # Progress snapshot (kept as return value rather than printing).
    return "".join(recovered)


if __name__ == "__main__":
    import rsa

    n = 28282590191348679547
    e = 15780653617344828671
    plaintext = (
        "En un lugar de la Mancha, de cuyo nombre no quiero acordarme, "
        "no ha mucho tiempo que vivía un hidalgo de los de lanza en astillero, "
        "adarga antigua, rocín flaco y galgo corredor."
    )

    cipher = rsa.encrypt_string(plaintext, n, e, padding_digits=5)
    print(padding_bruteforce_attack(cipher, n, e, padding_digits=5))
