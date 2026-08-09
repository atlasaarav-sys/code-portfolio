"""Todo CLI app: add / list / done / remove / clear, persisted to JSON."""

import argparse

from storage import load_tasks, save_tasks, next_id


def cmd_add(args):
    tasks = load_tasks()
    task_id = next_id(tasks)
    from storage import Task
    tasks.append(Task(id=task_id, title=args.title, priority=args.priority))
    save_tasks(tasks)
    print(f"Added task #{task_id}: {args.title}")


def cmd_list(args):
    tasks = load_tasks()
    if not args.all:
        tasks = [t for t in tasks if not t.done]
    if not tasks:
        print("No tasks.")
        return
    for t in tasks:
        status = "x" if t.done else " "
        print(f"[{status}] #{t.id} ({t.priority}) {t.title}")


def cmd_done(args):
    tasks = load_tasks()
    for t in tasks:
        if t.id == args.id:
            t.done = True
            save_tasks(tasks)
            print(f"Marked #{args.id} done.")
            return
    print(f"No task with id {args.id}")


def cmd_remove(args):
    tasks = load_tasks()
    filtered = [t for t in tasks if t.id != args.id]
    if len(filtered) == len(tasks):
        print(f"No task with id {args.id}")
        return
    save_tasks(filtered)
    print(f"Removed #{args.id}")


def cmd_clear(args):
    save_tasks([])
    print("Cleared all tasks.")


def build_parser():
    parser = argparse.ArgumentParser(description="Simple todo list")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="add a task")
    p_add.add_argument("title")
    p_add.add_argument("--priority", default="normal", choices=["low", "normal", "high"])
    p_add.set_defaults(func=cmd_add)

    p_list = sub.add_parser("list", help="list tasks")
    p_list.add_argument("--all", action="store_true", help="include done tasks")
    p_list.set_defaults(func=cmd_list)

    p_done = sub.add_parser("done", help="mark task done")
    p_done.add_argument("id", type=int)
    p_done.set_defaults(func=cmd_done)

    p_remove = sub.add_parser("remove", help="remove a task")
    p_remove.add_argument("id", type=int)
    p_remove.set_defaults(func=cmd_remove)

    p_clear = sub.add_parser("clear", help="remove all tasks")
    p_clear.set_defaults(func=cmd_clear)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
