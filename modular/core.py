"""Core number theory and modular arithmetic routines.

This module intentionally avoids any I/O so it can be imported from scripts.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isqrt
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np


def is_prime(n: int) -> bool:
    """Return True if n is prime (deterministic trial division)."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    limit = isqrt(n)
    for candidate in range(3, limit + 1, 2):
        if n % candidate == 0:
            return False
    return True


def list_primes(start: int, end: int) -> List[int]:
    """List primes in the interval [start, end)."""
    if end <= 2:
        return []

    sieve = [1 for _ in range(end)]
    sieve[0] = 0
    if end > 1:
        sieve[1] = 0

    limit = int(end**0.5)
    candidate = 2
    while candidate <= limit:
        if sieve[candidate] == 0:
            candidate += 1
            continue

        multiple = candidate * 2
        while multiple < end:
            sieve[multiple] = 0
            multiple += candidate

        candidate += 1

    primes: List[int] = []
    for value in range(max(2, start), end):
        if sieve[value] == 1:
            primes.append(value)
    return primes


def gcd(a: int, b: int) -> int:
    """Greatest common divisor using Euclid's algorithm."""
    x, y = abs(a), abs(b)
    while y != 0:
        x, y = y, x % y
    return x


def bezout(a: int, b: int) -> Tuple[int, int, int]:
    """Extended Euclid.

    Returns (g, x, y) such that x*a + y*b = g = gcd(a, b).
    """
    if a == 0 and b == 0:
        return 0, 0, 0

    # Preserve the original logic (vector-based) but with clearer names.
    larger = a if a > b else b
    smaller = b if a > b else a

    vec_larger = np.array([1, 0], dtype=object)
    vec_smaller = np.array([0, 1], dtype=object)

    while smaller != 0:
        quotient = larger // smaller
        larger, smaller = smaller, larger % smaller
        vec_larger, vec_smaller = vec_smaller, vec_larger - (quotient * vec_smaller)

    if a > b:
        return int(larger), int(vec_larger[0]), int(vec_larger[1])
    return int(larger), int(vec_larger[1]), int(vec_larger[0])


def are_coprime(a: int, b: int) -> bool:
    """Return True if gcd(a, b) == 1."""
    return gcd(a, b) == 1


def mod_pow(base: int, exponent: int, modulus: int) -> int:
    """Compute base**exponent mod modulus (supports negative exponent)."""
    if modulus == 0:
        raise ValueError("modulus must be non-zero")

    if exponent < 0:
        base = mod_inverse(base, modulus)
        if base is None:
            raise ValueError("base has no modular inverse for negative exponent")
        exponent = -exponent

    return pow(base % modulus, exponent, modulus)


def mod_inverse(value: int, modulus: int) -> Optional[int]:
    """Return the modular inverse of value modulo modulus, or None if it doesn't exist."""
    g, x, _y = bezout(value, modulus)
    if g != 1:
        return None
    return x % modulus


def _rho_polynomial(x: int, c: int, n: int) -> int:
    return (x * x + c) % n


def _pollards_rho(n: int) -> int:
    """Pollard's rho: returns a non-trivial factor of n, or n if it fails."""
    if n % 2 == 0:
        return 2

    c = 1
    while True:
        x = 2
        y = 2
        d = 1
        while d == 1:
            x = _rho_polynomial(x, c, n)
            y = _rho_polynomial(_rho_polynomial(y, c, n), c, n)
            d = gcd(abs(x - y), n)

        if d != n:
            return d

        c += 1
        if c > 100:
            return n


def factorize(n: int) -> Dict[int, int]:
    """Return the prime factorization of n as {prime: exponent}."""
    if n <= 1:
        return {}

    remaining = n
    factors: Dict[int, int] = {}

    # Fast trial division for small-ish n.
    if remaining < 10**7:
        candidate = 2
        while candidate * candidate <= remaining:
            while remaining % candidate == 0:
                factors[candidate] = factors.get(candidate, 0) + 1
                remaining //= candidate
            candidate = 3 if candidate == 2 else candidate + 2

        if remaining != 1:
            factors[remaining] = factors.get(remaining, 0) + 1
        return factors

    while remaining != 1:
        d = _pollards_rho(remaining)
        if d == remaining:
            # Fallback: treat the remainder as prime (or a hard composite)
            factors[remaining] = factors.get(remaining, 0) + 1
            break

        remaining //= d

        if is_prime(d):
            factors[d] = factors.get(d, 0) + 1
        else:
            sub = factorize(d)
            for p, exp in sub.items():
                factors[p] = factors.get(p, 0) + exp

        if remaining != 1 and is_prime(remaining):
            factors[remaining] = factors.get(remaining, 0) + 1
            remaining = 1

    return factors


def euler_totient(n: int) -> int:
    """Euler's totient function φ(n)."""
    if n <= 0:
        raise ValueError("n must be positive")
    if n == 1:
        return 1

    factors = factorize(n)

    result = n
    for p in factors.keys():
        result = result // p * (p - 1)
    return result


def legendre_symbol(a: int, p: int) -> int:
    """Compute the Legendre symbol (a|p) for odd prime p."""
    value = mod_pow(a, (p - 1) // 2, p)
    if value == p - 1:
        return -1
    return int(value)


def solve_congruence_system(
    a_list: Sequence[int],
    b_list: Sequence[int],
    p_list: Sequence[int],
) -> Tuple[int, int]:
    """Solve the system a_i * x = b_i (mod p_i) using CRT.

    Returns (x, N) where N = Π p_i and x is the solution modulo N.
    """
    if not (len(a_list) == len(b_list) == len(p_list)):
        raise ValueError("a_list, b_list and p_list must have the same length")

    modulus_product = 1
    for p in p_list:
        modulus_product *= p

    x = 0
    for a_i, b_i, p_i in zip(a_list, b_list, p_list):
        n_i = modulus_product // p_i
        inv_n_i = mod_inverse(n_i, p_i)
        inv_a_i = mod_inverse(a_i, p_i)
        if inv_n_i is None or inv_a_i is None:
            raise ValueError("system is not solvable with given moduli")

        x += (b_i * inv_a_i) * n_i * inv_n_i

    return int(x % modulus_product), int(modulus_product)


def mod_sqrt(n: int, p: int) -> Optional[int]:
    """Return a square root of n modulo p, or None if it doesn't exist.

    Note: this keeps the original 'Cipolla-like' approach used in the lab code.
    """
    if legendre_symbol(n, p) != 1:
        return None

    a = 0
    for i in range(1, p):
        if legendre_symbol((i * i - n) % p, p) == -1:
            a = i
            w = ((a * a - n) % p) ** (1 / 2)
            break
    else:
        return None

    x = (a + w) ** ((p + 1) // 2)

    if isinstance(x, complex):
        # Keep the original parsing approach.
        try:
            x = float(str(x).split("(")[1].split("+")[0].split("-")[0])
        except Exception:
            x = float(str(x).split("(")[1].split("+")[0])

    return int(round(x)) % p


def quadratic_equation_mod_p(a: int, b: int, c: int, p: int) -> Tuple[int, int]:
    """Solve a*x^2 + b*x + c = 0 (mod p) for prime p."""
    disc = (b * b - 4 * a * c) % p
    root = mod_sqrt(disc, p)
    if root is None:
        raise ValueError("no square root exists for the discriminant")

    inv_2a = mod_inverse(2 * a, p)
    if inv_2a is None:
        raise ValueError("2*a has no inverse modulo p")

    x = ((-b + root) * inv_2a) % p
    y = ((-b - root) * inv_2a) % p
    return int(x), int(y)
