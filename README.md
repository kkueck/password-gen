# Terminal Password Generator

A secure, lightweight, and modern terminal password generator written in Python. It generates cryptographically secure, high-entropy passwords using Python's built-in `secrets` module and requires **zero external dependencies**.

---

## 🚀 Features

- **Interactive Terminal UI**: Prompts for password length (with a sensible default of 16 characters) and validates input.
- **Cryptographically Secure**: Powered by Python's `secrets` module (`SystemRandom`), suitable for handling sensitive authentication credentials.
- **Complex Passwords by Default**: Guarantees at least one uppercase letter, lowercase letter, number, and special character.
- **Strength & Entropy Analysis**: Calculates information entropy in bits and rates password strength (Weak, Moderate, Strong, Very Strong).
- **Clipboard Integration**: Automatically copies passwords to clipboard on macOS (`pbcopy`), Linux (`wl-copy`/`xclip`), or Windows (`clip`).
- **Flexible CLI Flags**: Run non-interactively in scripts or generate multiple passwords in batch mode.
- **Pure Python 3 Standard Library**: No `pip install` required.

---

## 💻 How to Run

### Interactive Mode (Default)

Run the application directly in your terminal:

```bash
python3 main.py
```

or using the convenience script:

```bash
./password_generator.py
```

**Example interactive session:**
```text
╔═══════════════════════════════════════════════╗
║       🔐 SECURE PASSWORD GENERATOR          ║
║     Cryptographically Secure & Custom       ║
╚═══════════════════════════════════════════════╝

Enter desired password length [16]: 20

┌═════════════════════════════════════════════════════════════┐
│ Your Generated Password:                                    │
│   Ue0U%){*U.$[gxgUudm*                                      │
├═════════════════════════════════════════════════════════════┤
│  Length: 20 chars  |  Entropy: 129.5 bits  |  [Very Strong] │
└═════════════════════════════════════════════════════════════┘
 ✔ Lowercase (a-z)   ✔ Uppercase (A-Z)   ✔ Digits (0-9)   ✔ Symbols (!@#$)

📋 Password automatically copied to your clipboard!

Generate another password? [Y/n]: 
```

---

## ⚙️ Command-Line Options

You can also bypass interactive prompts by passing flags:

| Option | Description |
|---|---|
| `-l, --length <N>` | Desired password length (e.g., `-l 24`) |
| `-c, --count <N>` | Generate multiple passwords at once (e.g., `-c 5`) |
| `--copy` | Automatically copy single password to clipboard |
| `--no-symbols` | Exclude special characters/punctuation |
| `--no-digits` | Exclude numbers |
| `--no-upper` | Exclude uppercase letters |
| `--exclude-ambiguous` | Exclude visually ambiguous characters (`1`, `l`, `I`, `0`, `O`) |
| `-h, --help` | Show help message |

### Examples

Generate a 24-character password:
```bash
python3 main.py -l 24
```

Generate 5 passwords of length 16:
```bash
python3 main.py -l 16 -c 5
```

Generate a 20-character password without ambiguous characters:
```bash
python3 main.py -l 20 --exclude-ambiguous
```

---

## 🧪 Running Tests

To run the unit test suite:

```bash
python3 test_generator.py
```
