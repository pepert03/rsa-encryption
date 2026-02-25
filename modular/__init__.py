"""modular package

Number theory and modular arithmetic helpers used by IMAT-LAB and RSA utilities.

Public API is re-exported from :mod:`modular.core`.
"""

from .core import (
    are_coprime,
    bezout,
    euler_totient,
    factorize,
    gcd,
    is_prime,
    legendre_symbol,
    list_primes,
    mod_inverse,
    mod_pow,
    mod_sqrt,
    quadratic_equation_mod_p,
    solve_congruence_system,
)

__all__ = [
    "are_coprime",
    "bezout",
    "euler_totient",
    "factorize",
    "gcd",
    "is_prime",
    "legendre_symbol",
    "list_primes",
    "mod_inverse",
    "mod_pow",
    "mod_sqrt",
    "quadratic_equation_mod_p",
    "solve_congruence_system",
]
