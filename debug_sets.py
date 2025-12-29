"""Quick test to find the set that's causing JSON serialization issues."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from seedworld.generator_v2 import generate_v2
import json

# Generate a spec
spec = generate_v2(12345)

# Try to find what's causing the issue
def find_sets(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            find_sets(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            find_sets(v, f"{path}[{i}]")
    elif isinstance(obj, set):
        print(f"Found set at: {path}")
        print(f"  Contents: {obj}")

print("Looking for sets in the spec...")
find_sets(spec)
