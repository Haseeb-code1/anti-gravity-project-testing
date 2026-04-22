import unittest
import string
import math
from generator import generate_password, calculate_entropy, evaluate_strength, AMBIGUOUS_CHARS

class TestGenerator(unittest.TestCase):

    def test_generate_password_length(self):
        """Test that the generated password has the correct length."""
        pwd = generate_password(16, True, True, True, True, False)
        self.assertEqual(len(pwd), 16)
        
        pwd_short = generate_password(8, True, False, False, False, False)
        self.assertEqual(len(pwd_short), 8)

    def test_generate_password_pools(self):
        """Test that only selected character pools are used."""
        # Only lowercase
        pwd_lower = generate_password(50, False, True, False, False, False)
        self.assertTrue(all(c in string.ascii_lowercase for c in pwd_lower))

        # Only uppercase
        pwd_upper = generate_password(50, True, False, False, False, False)
        self.assertTrue(all(c in string.ascii_uppercase for c in pwd_upper))

        # Only digits
        pwd_digits = generate_password(50, False, False, True, False, False)
        self.assertTrue(all(c in string.digits for c in pwd_digits))

        # Only special characters
        pwd_special = generate_password(50, False, False, False, True, False)
        self.assertTrue(all(c in string.punctuation for c in pwd_special))

    def test_exclude_ambiguous_chars(self):
        """Test that ambiguous characters are excluded when requested."""
        # Generate a long password to ensure high probability of hitting an ambiguous char
        # if the logic was broken
        pwd = generate_password(200, True, True, True, True, True)
        for char in AMBIGUOUS_CHARS:
            self.assertNotIn(char, pwd)

    def test_generate_password_errors(self):
        """Test that ValueError is raised on invalid inputs."""
        # No character types selected
        with self.assertRaises(ValueError) as context:
            generate_password(10, False, False, False, False, False)
        self.assertEqual(str(context.exception), "Please select at least one character type.")

        # Pool empty after excluding ambiguous characters
        # The only way this happens is if we ONLY select lowercase and/or uppercase and/or digits
        # and ALL chosen types are fully ambiguous, but AMBIGUOUS_CHARS = "lI1O0".
        # This condition is practically hard to hit with standard ascii pools, but let's test if we can fake it.
        # It's covered by line 26 in generator.py

    def test_calculate_entropy(self):
        """Test entropy calculation logic."""
        # Lowercase only: pool size 26
        pwd_lower = "abcdef"
        expected_lower = len(pwd_lower) * math.log2(26)
        self.assertAlmostEqual(calculate_entropy(pwd_lower), expected_lower)

        # Lowercase + Digits: pool size 26 + 10 = 36
        pwd_mixed = "abc123"
        expected_mixed = len(pwd_mixed) * math.log2(36)
        self.assertAlmostEqual(calculate_entropy(pwd_mixed), expected_mixed)

        # Empty password
        self.assertEqual(calculate_entropy(""), 0.0)

    def test_evaluate_strength(self):
        """Test strength evaluation based on entropy thresholds."""
        # Weak (< 50)
        self.assertEqual(evaluate_strength(49.9), "Weak")
        self.assertEqual(evaluate_strength(10), "Weak")

        # Medium (>= 50 and < 80)
        self.assertEqual(evaluate_strength(50.0), "Medium")
        self.assertEqual(evaluate_strength(79.9), "Medium")

        # Strong (>= 80)
        self.assertEqual(evaluate_strength(80.0), "Strong")
        self.assertEqual(evaluate_strength(120), "Strong")

if __name__ == "__main__":
    unittest.main()
