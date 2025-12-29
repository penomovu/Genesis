from __future__ import annotations

import argparse
import sys

from .generator import generate, to_json


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a seed-based game blueprint as JSON")
    parser.add_argument("seed", type=int, nargs="?", default=104729)
    args = parser.parse_args(argv)

    spec = generate(args.seed)
    sys.stdout.write(to_json(spec))
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
