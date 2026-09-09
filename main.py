#!/usr/bin/env python3
"""Interactive Terminal Password Generator Application."""

from __future__ import annotations

import argparse
import os
import platform
import re
import subprocess
import sys

from generator import generate_password

ANSI_REGEX = re.compile(r"\x1b\[[0-9;]*m")

# ANSI Styling Codes
USE_COLOR = sys.stdout.isatty() and not os.environ.get("NO_COLOR")


def colorize(text: str, code: str) -> str:
    if not USE_COLOR:
        return text
    return f"{code}{text}\033[0m"


def bold(text: str) -> str:
    return colorize(text, "\033[1m")


def green(text: str) -> str:
    return colorize(text, "\033[32m")


def cyan(text: str) -> str:
    return colorize(text, "\033[36m")


def yellow(text: str) -> str:
    return colorize(text, "\033[33m")


def red(text: str) -> str:
    return colorize(text, "\033[31m")


def magenta(text: str) -> str:
    return colorize(text, "\033[35m")


def copy_to_clipboard(text: str) -> bool:
    """Copy given text to system clipboard using native platform tools."""
    system = platform.system()
    try:
        if system == "Darwin":
            proc = subprocess.Popen(["pbcopy"], stdin=subprocess.PIPE)
            proc.communicate(input=text.encode("utf-8"))
            return proc.returncode == 0
        elif system == "Linux":
            for cmd in [["wl-copy"], ["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"]]:
                try:
                    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
                    proc.communicate(input=text.encode("utf-8"))
                    if proc.returncode == 0:
                        return True
                except FileNotFoundError:
                    continue
        elif system == "Windows":
            proc = subprocess.Popen(["clip"], stdin=subprocess.PIPE)
            proc.communicate(input=text.encode("utf-8"))
            return proc.returncode == 0
    except Exception:
        return False
    return False


def print_banner() -> None:
    banner = f"""
{cyan("╔═══════════════════════════════════════════════╗")}
{cyan("║")}       {bold("🔐 SECURE PASSWORD GENERATOR")}          {cyan("║")}
{cyan("║")}     {magenta("Cryptographically Secure & Custom")}       {cyan("║")}
{cyan("╚═══════════════════════════════════════════════╝")}
"""
    print(banner)


def visible_length(text: str) -> int:
    """Return the length of the string excluding ANSI escape codes."""
    return len(ANSI_REGEX.sub("", text))


def display_password_card(password: str, entropy: float, strength: str) -> None:
    """Display the generated password in a formatted terminal card."""
    strength_colors = {
        "Weak": red,
        "Moderate": yellow,
        "Strong": green,
        "Very Strong": cyan,
    }
    color_func = strength_colors.get(strength, green)
    colored_strength = color_func(f"[{strength}]")

    title = " Your Generated Password:"
    pwd_display = f"   {bold(green(password))}"
    stats_display = f" Length: {len(password)} chars  |  Entropy: {entropy:.1f} bits  |  {colored_strength}"

    inner_width = max(
        visible_length(title),
        visible_length(pwd_display),
        visible_length(stats_display),
        54,
    ) + 2

    border = "═" * inner_width

    def print_line(content: str) -> None:
        pad = inner_width - visible_length(content)
        print(cyan("│") + content + (" " * max(0, pad)) + cyan("│"))

    print()
    print(cyan(f"┌{border}┐"))
    print_line(bold(title))
    print_line(pwd_display)
    print(cyan(f"├{border}┤"))
    print_line(f" {stats_display}")
    print(cyan(f"└{border}┘"))
    print(f" {green('✔')} Lowercase (a-z)   {green('✔')} Uppercase (A-Z)   {green('✔')} Digits (0-9)   {green('✔')} Symbols (!@#$)")
    print()


def prompt_password_length(default: int = 16) -> int:
    """Prompt the user interactively for the desired password length."""
    while True:
        try:
            prompt_text = f"Enter desired password length [{bold(str(default))}]: "
            raw_input = input(prompt_text).strip()

            if not raw_input:
                return default

            length = int(raw_input)
            if length < 4:
                print(yellow("⚠️  Length must be at least 4 to include lowercase, uppercase, digit, and symbol."))
                continue
            if length > 256:
                confirm = input(yellow(f"⚠️  Length {length} is very large. Proceed? [y/N]: ")).strip().lower()
                if confirm != "y":
                    continue
            return length
        except ValueError:
            print(red("❌ Invalid number. Please enter a positive integer (e.g., 16, 24, 32)."))
        except (KeyboardInterrupt, EOFError):
            print("\n\nExiting...")
            sys.exit(0)


def interactive_loop() -> None:
    """Run the interactive terminal interface."""
    print_banner()

    default_length = 16
    while True:
        length = prompt_password_length(default=default_length)
        default_length = length

        password, entropy, strength = generate_password(length=length)
        display_password_card(password, entropy, strength)

        # Offer clipboard copy if available
        copied = copy_to_clipboard(password)
        if copied:
            print(f"📋 {green('Password automatically copied to your clipboard!')}")
        else:
            print(f"💡 {yellow('Tip: Select and copy the password above.')}")

        # Prompt for next action
        try:
            print()
            again = input("Generate another password? [Y/n]: ").strip().lower()
            if again in ("n", "no", "q", "quit", "exit"):
                print(f"\n{cyan('Stay secure! Goodbye. 👋')}\n")
                break
            print("\n" + "─" * 48 + "\n")
        except (KeyboardInterrupt, EOFError):
            print(f"\n\n{cyan('Goodbye! 👋')}\n")
            break


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate cryptographically secure passwords inside your terminal.",
    )
    parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=None,
        help="Desired password length (defaults to interactive prompt if omitted).",
    )
    parser.add_argument(
        "-c",
        "--count",
        type=int,
        default=1,
        help="Number of passwords to generate (default: 1).",
    )
    parser.add_argument(
        "--no-symbols",
        action="store_true",
        help="Do not include symbols in generated password.",
    )
    parser.add_argument(
        "--no-digits",
        action="store_true",
        help="Do not include numbers in generated password.",
    )
    parser.add_argument(
        "--no-upper",
        action="store_true",
        help="Do not include uppercase letters.",
    )
    parser.add_argument(
        "--exclude-ambiguous",
        action="store_true",
        help="Exclude ambiguous characters (e.g. 1, l, I, 0, O).",
    )
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy password to clipboard.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    # If no length argument was specified on CLI, run interactive mode
    if args.length is None:
        interactive_loop()
        return

    # CLI non-interactive mode
    if args.length < 1:
        print(red("Error: Password length must be at least 1."), file=sys.stderr)
        sys.exit(1)

    for i in range(args.count):
        try:
            pwd, entropy, strength = generate_password(
                length=args.length,
                include_uppercase=not args.no_upper,
                include_lowercase=True,
                include_digits=not args.no_digits,
                include_symbols=not args.no_symbols,
                exclude_ambiguous=args.exclude_ambiguous,
            )
            if args.count == 1:
                display_password_card(pwd, entropy, strength)
                if args.copy:
                    if copy_to_clipboard(pwd):
                        print(f"📋 {green('Copied to clipboard!')}")
            else:
                print(f"{i + 1:2d}. {bold(pwd)}  ({entropy:.1f} bits, {strength})")
        except ValueError as e:
            print(red(f"Error: {e}"), file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nExiting...")
        sys.exit(0)
