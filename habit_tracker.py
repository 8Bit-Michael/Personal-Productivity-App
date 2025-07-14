from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from colorama import init, Fore
from difflib import get_close_matches
from pathlib import Path

init(autoreset=True)

def match_input(user_input, options, cutoff=0.6):
    return get_close_matches(user_input.lower(), options, n=1, cutoff=cutoff)

class Habit:
    FREQ_DELTAS = {
        "daily": timedelta(days=1),
        "weekly": timedelta(weeks=1),
        "monthly": relativedelta(months=1),
        "yearly": relativedelta(years=1)
    }

    def __init__(self, name, frequency, streak=0, last_completed=None):
        self.name = name
        self.frequency = frequency
        self.streak = streak
        self.last_completed = last_completed or datetime.now()

    def to_dict(self):
        return {
            "name": self.name,
            "frequency": self.frequency,
            "streak": self.streak,
            "last_completed": self.last_completed.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            frequency=data["frequency"],
            streak=data["streak"],
            last_completed=datetime.fromisoformat(data["last_completed"])
        )

    def mark_completed(self):
        now = datetime.now()
        delta = now - self.last_completed
        freq_delta = self.FREQ_DELTAS[self.frequency]
        
        if isinstance(freq_delta, relativedelta):
            freq_delta = now - (now - freq_delta)
        if delta <= freq_delta:
            self.streak += 1
            print(Fore.GREEN + f"Streak continued! {self.streak} in a row.")
        else:
            self.streak = 1
            print(Fore.YELLOW + "Missed frequency window — streak reset to 1.")
        self.last_completed = now

class HabitTracker:
    def __init__(self, habits=None):
        self.habits = habits or []

    def add_habit(self):
        name = input("Name of habit: ").strip()
        freq_in = input("Frequency ('daily', 'weekly', 'monthly', 'yearly'): ").strip()
        refined = match_input(freq_in, list(Habit.FREQ_DELTAS.keys()))
        if not refined:
            print(Fore.RED + "Invalid frequency.")
            return
        habit = Habit(name, refined[0])
        self.habits.append(habit)
        print(Fore.GREEN + f"Habit '{name}' added with '{refined[0]}' frequency.")

    def list_habits(self):
        if not self.habits:
            print(Fore.YELLOW + "No habits yet.")
            return
        for h in self.habits:
            print(f"- {h.name} | {h.frequency} | streak: {h.streak} | last: {h.last_completed:%Y-%m-%d %H:%M}")

    def mark_habit(self):
        name = input("Which habit to mark complete? ").strip()
        for h in self.habits:
            if match_input(name, [h.name]):
                h.mark_completed()
                return
        print(Fore.RED + "No matching habit.")

    def save(self, username):
        from storage import save_habits
        path = Path("data") / username / "habits.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        save_habits(self.habits, path)
        print(Fore.GREEN + "Habits saved.")

    def load(self, username):
        from storage import load_habits
        path = Path("data") / username / "habits.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        self.habits = load_habits(path)
        print(Fore.GREEN + "Habits loaded.")
