import sys

from configs.parser import Parser, ParserError
from planner.palnner import Planner
from ui.visualizer import Visualizer  # adjust path to wherever Visualizer lives


def print_turn_logs(state: list[dict[int, str]]) -> None:
    for turn_idx in range(1, len(state)):
        prev = state[turn_idx - 1]
        curr = state[turn_idx]
        moves = []
        for did, pos in curr.items():
            if pos != prev.get(did):
                moves.append(f"D{did}-{pos}")
        line = " ".join(moves)
        if line:
            print(line)


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: python main.py <map_file>")
        sys.exit(1)

    try:
        map_obj = Parser(sys.argv[1]).parse()
    except ParserError as e:
        print(f"Parsing error: {e}")
        sys.exit(1)

    planner = Planner(map_obj)
    state = planner.plan()

    print_turn_logs(state)

    viz = Visualizer(map_obj)
    viz.run(state)
    print(len(state))


if __name__ == "__main__":
    main()