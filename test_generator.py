"""Unit tests for the password generator logic."""

import string
import unittest

from generator import (
    AMBIGUOUS_CHARS,
    DEFAULT_SYMBOLS,
    calculate_entropy,
    generate_password,
    get_strength_assessment,
)


class TestPasswordGenerator(unittest.TestCase):
    def test_default_generation(self):
        pwd, entropy, strength = generate_password()
        self.assertEqual(len(pwd), 16)
        self.assertTrue(any(c in string.ascii_lowercase for c in pwd))
        self.assertTrue(any(c in string.ascii_uppercase for c in pwd))
        self.assertTrue(any(c in string.digits for c in pwd))
        self.assertTrue(any(c in DEFAULT_SYMBOLS for c in pwd))
        self.assertGreater(entropy, 60)

    def test_custom_length(self):
        for length in [8, 12, 24, 64, 128]:
            pwd, _, _ = generate_password(length=length)
            self.assertEqual(len(pwd), length)

    def test_minimum_length_with_all_categories(self):
        pwd, _, _ = generate_password(length=4)
        self.assertEqual(len(pwd), 4)
        self.assertTrue(any(c in string.ascii_lowercase for c in pwd))
        self.assertTrue(any(c in string.ascii_uppercase for c in pwd))
        self.assertTrue(any(c in string.digits for c in pwd))
        self.assertTrue(any(c in DEFAULT_SYMBOLS for c in pwd))

    def test_invalid_length_error(self):
        with self.assertRaises(ValueError):
            generate_password(length=0)
        with self.assertRaises(ValueError):
            generate_password(length=-5)
        with self.assertRaises(ValueError):
            generate_password(length=3)  # Needs at least 4 when 4 categories selected

    def test_exclude_ambiguous_characters(self):
        for _ in range(20):
            pwd, _, _ = generate_password(length=50, exclude_ambiguous=True)
            for ch in AMBIGUOUS_CHARS:
                self.assertNotIn(ch, pwd)

    def test_toggle_character_sets(self):
        # Digits and lowercase only
        pwd, _, _ = generate_password(
            length=10,
            include_uppercase=False,
            include_symbols=False,
        )
        self.assertEqual(len(pwd), 10)
        self.assertTrue(all(c in string.ascii_lowercase + string.digits for c in pwd))
        self.assertFalse(any(c in string.ascii_uppercase for c in pwd))
        self.assertFalse(any(c in DEFAULT_SYMBOLS for c in pwd))

    def test_no_category_selected(self):
        with self.assertRaises(ValueError):
            generate_password(
                include_lowercase=False,
                include_uppercase=False,
                include_digits=False,
                include_symbols=False,
            )

    def test_entropy_and_strength_scale(self):
        self.assertEqual(get_strength_assessment(30)[0], "Weak")
        self.assertEqual(get_strength_assessment(50)[0], "Moderate")
        self.assertEqual(get_strength_assessment(70)[0], "Strong")
        self.assertEqual(get_strength_assessment(95)[0], "Very Strong")

    def test_uniqueness(self):
        passwords = {generate_password(length=16)[0] for _ in range(100)}
        self.assertEqual(len(passwords), 100)


if __name__ == "__main__":
    unittest.main()
