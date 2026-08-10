"""JSON-backed persistence for the todo app."""

from dataclasses import dataclass, asdict
from pathlib import Path
import json

DEFAULT_PATH = Path(__file__).parent / "tasks.json"


@dataclass
class Task:
    id: int
    title: str
    priority: str = "normal"
    done: bool = False


def load_tasks(path: Path = DEFAULT_PATH) -> list[Task]:
    if not path.exists():
        return []
    with open(path) as f:
        raw = json.load(f)
    return [Task(**item) for item in raw]


def save_tasks(tasks: list[Task], path: Path = DEFAULT_PATH) -> None:
    with open(path, "w") as f:
        json.dump([asdict(t) for t in tasks], f, indent=2)


def next_id(tasks: list[Task]) -> int:
    return max((t.id for t in tasks), default=0) + 1
