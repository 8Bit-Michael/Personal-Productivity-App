from datetime import datetime
from colorama import init, Fore
from difflib import get_close_matches
from pathlib import Path

init(autoreset=True)

def match_input(user_input, options, cutoff=0.6):
    return get_close_matches(user_input.lower(), options, n=1, cutoff=cutoff)

class Task:
    def __init__(self, title, due_date, priority_level, status):
        self.title = title
        self.due_date = self.parse_strict_date(due_date)
        self.priority_level = float(priority_level)
        self.status = status

    @staticmethod
    def parse_strict_date(date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except Exception:
            raise ValueError(Fore.RED + "Date must be YYYY‑MM‑DD and valid.")

    def information_review(self):
        print(Fore.GREEN + f"Task added: {self.title} | Due: {self.due_date:%Y‑%m‑%d} | Priority: {self.priority_level} | Status: {self.status}")

    def status_update(self):
        while True:
            stat = input("Set status ('pending', 'done', or 'exit'): ").strip()
            refined = match_input(stat, ['pending', 'done', 'exit'])
            if refined:
                if refined[0] in ('pending', 'done'):
                    self.status = refined[0]
                    print(Fore.GREEN + f"'{self.title}' marked {self.status}.")
                return

    def to_dict(self):
        return {
            "title": self.title,
            "due_date": self.due_date.isoformat(),
            "priority_level": self.priority_level,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            due_date=datetime.fromisoformat(data["due_date"]).strftime("%Y-%m-%d"),
            priority_level=data["priority_level"],
            status=data["status"]
        )

class TaskManager:
    def __init__(self, tasks, user_name):
        self.tasks = tasks or []
        self.user_name = user_name

    def add_task(self):
        while True:
            title = input("Task title: ").strip()
            due = input("Due date (YYYY‑MM‑DD): ").strip()
            try:
                Task.parse_strict_date(due)
            except ValueError as e:
                print(e)
                continue

            prio = input("Priority 0‑5: ").strip()
            try:
                if not (0 <= float(prio) <= 5):
                    raise ValueError
            except:
                print(Fore.RED + "Please enter a number between 0 and 5.")
                continue

            stat_in = input("Status ('pending' or 'done'): ").strip()
            refined = match_input(stat_in, ['pending', 'done'])
            if not refined:
                print(Fore.RED + "Status must be 'pending' or 'done'.")
                continue

            task = Task(title, due, prio, refined[0])
            if task.title in [t.title for t in self.tasks]:
                print(Fore.RED + "Task title already exists.")
                return
            task.information_review()
            self.tasks.append(task)
            return

    def remove_task(self):
        name = input("Title of task to remove: ").strip()
        for t in self.tasks:
            if match_input(name, [t.title]):
                self.tasks.remove(t)
                print(Fore.GREEN + f"Removed task '{t.title}'.")
                return
        print(Fore.RED + "No matching task found.")

    def list_tasks(self):
        if not self.tasks:
            print(Fore.YELLOW + "No tasks available.")
            return
        print(Fore.GREEN + f"Tasks for {self.user_name}:")
        for t in self.tasks:
            print(f"- {t.title} | Due: {t.due_date:%Y‑%m‑%d} | Priority: {t.priority_level} | Status: {t.status}")

    def mark_task(self):
        name = input("Which task to update status? ").strip()
        for t in self.tasks:
            if match_input(name, [t.title]):
                t.status_update()
                return
        print(Fore.RED + "No matching task found.")

    def sort_tasks(self):
        mode = input("Sort by 'priority' or 'date': ").strip()
        refined = match_input(mode, ['priority', 'date'])
        if not refined:
            print(Fore.RED + "Invalid sort option.")
            return
        if refined[0] == 'priority':
            sorted_tasks = sorted(self.tasks, key=lambda t: t.priority_level, reverse=True)
        else:
            sorted_tasks = sorted(self.tasks, key=lambda t: t.due_date)
        print(Fore.GREEN + f"Tasks sorted by {refined[0]}:")
        for t in sorted_tasks:
            print(f"- {t.title} | Due: {t.due_date:%Y‑%m‑%d} | Priority: {t.priority_level}")

    def save_to_file(self):
        from storage import save_tasks
        path = Path("data") / self.user_name / "tasks.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        save_tasks(self.tasks, path)
        print(Fore.GREEN + "Tasks saved.")

    def load_from_file(self):
        from storage import load_tasks
        path = Path("data") / self.user_name / "tasks.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        self.tasks = load_tasks(path)
        print(Fore.GREEN + "Tasks loaded.")

        
