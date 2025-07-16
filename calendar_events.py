from datetime import datetime
from colorama import init, Fore
from dateutil.relativedelta import relativedelta
from difflib import get_close_matches
from pathlib import Path

def match_input(user_input, options, cutoff=0.6):
    return get_close_matches(user_input.lower(), options, n=1, cutoff=cutoff)


init(autoreset=True)

class Event:
    def __init__(self, title, date, description):
        self.title = title
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            "title": self.title,
            "date": self.date,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data["title"],
            date=datetime.fromisoformat(data["date"]).strftime("%Y-%m-%d"),
            description=data["description"],
        )
    
    @staticmethod
    def parse_strict_date(date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except Exception:
            raise ValueError(Fore.RED + "Date must be YYYY-MM-DD and valid.")

    def format(self):
        print(Fore.GREEN + f" - {self.title} | Date: {self.date} | Description: {self.description}")

class Calendar:
    def __init__(self):
        self.events = []

    def add_event(self):
        while True:
            title = input("Event title: ").strip()
            date = input("Date (YYYY-MM-DD): ").strip()
            try:
                Event.parse_strict_date(date)
            except ValueError as e:
                print(e)
                continue
            description = input("Please enter a brief description of your event: ").strip()
            if not isinstance(description, str) or any(char.isdigit() for char in description) or description == "":
                print(Fore.RED + f"'{description}' is not a valid input. Please type a valid string input.")
                continue

            event = Event(title, date, description)
            if event.title in [e.title for e in self.events]:
                print(Fore.RED + "Task title already exists.")
                return
            event.format()
            self.events.append(event)
            return


    def list_events(self):
        if not self.events:
            print(Fore.YELLOW + "No events available.")
            return
        now = datetime.now()
        found = False

        print(Fore.GREEN + "Your events for this week include the following: ")
        for e in self.events:
            event_date = datetime.strptime(e.date, "%Y-%m-%d")
            if now <= event_date < now + relativedelta(weeks=1):
                print(Fore.GREEN + f" - {e.title} | Date: {event_date:%Y-%m-%d} | Description: {e.description}")
                found = True

        if not found:
            print(" - None found.")

        print(Fore.GREEN + "Your events for this month include the following: ")
        for e in self.events:
            event_date = datetime.strptime(e.date, "%Y-%m-%d")
            if now <= event_date < now + relativedelta(months=1):
                print(Fore.GREEN + f" - {e.title} | Date: {event_date:%Y-%m-%d} | Description: {e.description}")
                found = True
            
        if not found:
            print(" - None found.")

        print(Fore.GREEN + "Your events for this year include the following: ")
        for e in self.events:
            event_date = datetime.strptime(e.date, "%Y-%m-%d")
            if now <= event_date < now + relativedelta(years=1):
                print(Fore.GREEN + f" - {e.title} | Date: {event_date:%Y-%m-%d} | Description: {e.description}")
                found = True
            
        if not found:
            print(" - None found.")

    def remove_event(self):
        while True:
            name = input("Title of event to remove: ").strip()
            for e in self.events:
                if name == e:
                    self.events.remove(e)
                    print(Fore.GREEN + f"Removed task '{e.title}'.")
                    return
            print(Fore.RED + "No matching event found.")

    def get_upcoming_events(self):
        while True:
            now = datetime.now()
            upcoming_range = input("By what range would you like to see your upcoming events(weekly, monthly or yearly): ")
            refined_range = match_input(upcoming_range, ['weekly', 'monthly', 'yearly'])
                
            found = False

            if refined_range[0] == 'weekly':
                print(Fore.GREEN + "Your events for this week include the following: ")
                for e in self.events:
                    event_date = datetime.strptime(e.date, "%Y-%m-%d")
                    if 0 <= (event_date - now).days < 7:
                        print(Fore.GREEN + f" - {e.title} | Date: {event_date:%Y-%m-%d} | Description: {e.description}")
                        found = True
                    
                if not found:
                    print("None found.")

                break

            elif refined_range[0] == 'monthly':
                print(Fore.GREEN + "Your events for this month include the following: ")
                for e in self.events:
                    event_date = datetime.strptime(e.date, "%Y-%m-%d")
                    if 0 <= (event_date - now).days < 30:
                        print(Fore.GREEN + f" - {e.title} | Date: {event_date:%Y-%m-%d} | Description: {e.description}")
                        found = True

                if not found:
                    print("None found.")
                    
                break

            elif refined_range[0] == 'yearly':
                print(Fore.GREEN + "Your events for this year include the following: ")
                for e in self.events:
                    event_date = datetime.strptime(e.date, "%Y-%m-%d")
                    if 0 <= (event_date - now).days < 365:
                        print(Fore.GREEN + f" - {e.title} | Date: {event_date:%Y-%m-%d} | Description: {e.description}")
                        found = True
                
                if not found:
                    print("None found.")
                    
                break
            
            else:
                print(Fore.RED + f"Sorry, '{upcoming_range}' is not a valid input, please try again.")
                continue
    
    def save(self, username):
        from storage import save_events
        path = Path("data") / username / "events.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        save_events(self.events, path)
        print(Fore.GREEN + "Events saved.")

    def load(self, username):
        from storage import load_events
        path = Path("data") / username / "events.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        self.events = load_events(path)
        print(Fore.GREEN + "Events loaded.")
