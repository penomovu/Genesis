import json
import unittest

from seedworld.generator import generate, to_json


class TestGeneratorDeterminism(unittest.TestCase):
    def test_same_seed_same_output(self) -> None:
        a = to_json(generate(12345))
        b = to_json(generate(12345))
        self.assertEqual(a, b)

    def test_output_is_json(self) -> None:
        payload = to_json(generate(999))
        parsed = json.loads(payload)
        self.assertIn("seed", parsed)
        self.assertIn("world", parsed)


if __name__ == "__main__":
    unittest.main()
