from seedworld import generate
from seedworld.generator import to_json


def run() -> None:
    spec = generate(104729)
    print(to_json(spec))


if __name__ == "__main__":
    run()
