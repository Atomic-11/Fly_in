from typing import Dict, List, Tuple


def build_state(
    timed_paths: Dict[int, List[Tuple[str, int]]],
    end_name: str,
) -> List[Dict[int, str]]:
    max_turn = max(path[-1][1] for path in timed_paths.values())

    per_drone: Dict[int, Dict[int, str]] = {}

    for did, timed_path in timed_paths.items():
        turn_label: Dict[int, str] = {timed_path[0][1]: timed_path[0][0]}

        for (h1, t1), (h2, t2) in zip(timed_path, timed_path[1:]):
            if h1 == h2:
                # wait-hop
                turn_label[t2] = h1
            elif t2 - t1 == 1:
                # normal / priority move, completes in one turn
                turn_label[t2] = h2
            else:
                # restricted move, multi-turn transit
                for t in range(t1 + 1, t2):
                    turn_label[t] = f"{h1}-{h2}"
                turn_label[t2] = h2

        # pad remaining turns with final position (end)
        last_turn = timed_path[-1][1]
        last_hub = timed_path[-1][0]
        for t in range(last_turn + 1, max_turn + 1):
            turn_label[t] = last_hub

        per_drone[did] = turn_label

    state: List[Dict[int, str]] = []
    for t in range(0, max_turn + 1):
        state.append({did: per_drone[did][t] for did in timed_paths})

    return state