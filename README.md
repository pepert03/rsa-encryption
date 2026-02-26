<div align="center">
  <img src="media/logo.svg" width="100" alt="RSA Chat Logo"/>

  # RSA-Encryption
  
  **A peer-to-peer chat application using RSA encryption with custom libraries for modular arithmetic**
  
  <p>
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
    <img src="https://img.shields.io/badge/Bun-%23000000.svg?style=for-the-badge&logo=bun&logoColor=white" alt="Bun"/>
    <img src="https://img.shields.io/badge/WebSockets-010101?style=for-the-badge&logo=socket.io&logoColor=white" alt="WebSockets"/>
    <img src="https://img.shields.io/badge/PyScript-000000?style=for-the-badge&logo=python&logoColor=white" alt="PyScript"/>
    <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white" alt="HTML5"/>
  </p>
</div>

---

An educational repository for **modular arithmetic and RSA**, including:

- A browser-based **CryptoChat P2P** client (PyScript/Pyodide) that encrypts/decrypts using Python.
- A **WebSocket relay server** (Bun) that broadcasts packets to connected peers.
- Python **libraries** (`modular` and `rsa`) plus demo/attack scripts.

> Disclaimer: this is **teaching code**, not production cryptography. It uses small keys and a simplistic per-character scheme with a decimal-suffix padding, which is vulnerable to multiple attacks.

## Components

### RSA algorithm (math overview)

RSA works over modular arithmetic.

**Key generation**

1. Choose two primes $p$ and $q$.
2. Compute:

$$
n = pq
$$

$$
\varphi(n) = (p-1)(q-1)
$$

3. Choose an exponent $e$ such that $\gcd(e, \varphi(n)) = 1$.
4. Compute the modular inverse $d$:

$$
d \equiv e^{-1} \pmod{\varphi(n)}
$$

Public key: $(n, e)$

Private key: $d$ (and implicitly $p, q$)

**Encryption / decryption**

Represent the plaintext as an integer $m$ with $0 \le m < n$.

$$
c \equiv m^e \pmod{n}
$$

$$
m \equiv c^d \pmod{n}
$$

This repo often encrypts **per character** (each Unicode codepoint separately). It also includes a simple teaching padding: append $p$ random decimal digits to $m$ before exponentiation, and remove them after decryption.

### 1) Web client (PyScript)

- File: `index.html`
- What it does:
  - Generates RSA keys in Python (inside the browser via Pyodide).
  - Broadcasts presence (name + public key) to the network.
  - Supports 1:1 chat: encrypts with the recipient public key and decrypts with your private key.
  - Keeps a “Global P2P Network” tab as an encrypted traffic monitor.

### 2) WebSocket relay (Bun)

- File: `server.ts`
- What it does:
  - Accepts WebSocket connections at `ws://localhost:3000`.
  - Subscribes clients to a global channel (`chat_global`).
  - Republishes messages to all subscribers (excluding the sender).

### 3) Python libraries

#### `modular/`

Number theory and modular arithmetic helpers.

- Entry point: `modular/__init__.py`
- Implementation: `modular/core.py`
- Includes: `gcd`, `bezout`, `mod_inverse`, `mod_pow`, `factorize`, `euler_totient`, CRT utilities, etc.

#### `rsa/`

Basic RSA utilities and the simple decimal-suffix padding.

- Entry point: `rsa/__init__.py`
- Implementation: `rsa/core.py`
- Includes: `generate_keys`, `encrypt_string`, `decrypt_string`, etc.

### 4) Extra scripts

- `rsa_attacks.py`: cryptanalysis helpers for small RSA (factoring-based key recovery, dictionary attack, padding brute force).
- `criptochat.py`: CLI version that stores contacts in `contactos.json` and messages in `.txt` files.
- `modular.py`: legacy/experimental script with similar routines (contains prints/tests at the end).
- `imatlab.py`, `imatlab_benchmark.py`: lab utilities/benchmarks.

## Requirements

- **Bun** (for the WebSocket relay).
- **Python 3.11+** (for Python scripts/libraries).
- Internet access to load PyScript from the CDN used in `index.html`.

If you use the Python libraries, `pyproject.toml` declares a dependency on `numpy`.

## Run the chat locally

1) Start the WebSocket relay:

```bash
bun run server.ts
```

2) Serve the static files (recommended; avoid opening `file://`):

```bash
python -m http.server 8000
```

3) Open the client:

- http://localhost:8000/index.html

4) In the UI:

- Set your public name and click **Go online**.
- Wait until it shows **Python Ready ✅**.
- Select an online user and send messages.

## Quick usage (Python)

Encrypt/decrypt example:

```python
import rsa

n, e, d = rsa.generate_keys(100, 500)
msg = "hello"

cipher = rsa.encrypt_string(msg, n, e, padding_digits=2)
plain = rsa.decrypt_string(cipher, n, d, padding_digits=2)
print(plain)
```

Recover `d` by factoring `n` (toy example):

```python
from rsa_attacks import recover_private_exponent

d = recover_private_exponent(n, e)
```

## Repo layout (at a glance)

- `index.html`: web client (PyScript) + UI.
- `server.ts`: WebSocket relay (Bun).
- `rsa/`: RSA package.
- `modular/`: modular arithmetic package.
- `rsa_attacks.py`: attacks/demos.
- `criptochat.py`: CLI + `contactos.json`.

## Security notes (important)

- Real RSA requires large keys (e.g. 2048+ bits) and standard padding (OAEP/PSS).
- Per-character encryption and ad-hoc decimal padding leak structure and are attackable.
- This project is meant to learn, experiment, and observe attacks in practice.
