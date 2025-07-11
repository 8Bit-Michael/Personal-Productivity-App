from colorama import init, Fore
from datetime import datetime, timedelta

init(autoreset=True)

class Habit:
    def __init__(self, name, frequency, streak, last_completed):
        self.name = name
        self.frequency = frequency
        self.streak = streak
        self.last_completed = last_completed
    
    def marked_completed(self, today):  
        today = datetime.now()
        time_passed = today - last_completed

        last_completed += 1
        self.reset_streak_if_needed()
        if self.streak == True:
            self.streak += 1                                 
            print(Fore.GREEN + f"You now have a {self.streak} {self.frequency} streak!")
        else:
            self.streak = 0
            print(Fore.RED + f"Your streak has been set to zero. Remember, consistency is key.")


    def reset_streak_if_needed(self, today):
        if self.frequency == 'daily':
            if self.time_passed > timedelta(hours=24):
                return False
            else:
                return True
        elif self.frequency == 'weekly':
            if self.time_passed > timedelta(hours=168):
                return False
            else:
                return True

    def to_dict(self):
        return {
            'Name': self.name,
            'Frequency': self.frequency,
            'Streak': self.streak,
            'Last completed': self.last_completed
        }

    def from_dict(cls, data):
        return cls(
            name=data['Name'],
            frequency=data['Frequency'],
            streak=data['Streak'],
            last_completed=data['Last completed']
            )