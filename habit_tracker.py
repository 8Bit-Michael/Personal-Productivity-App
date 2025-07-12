from colorama import init, Fore
from datetime import datetime, timedelta
from difflib import get_close_matches
from datetime import datetime
from dateutil.relativedelta import relativedelta
import re
import json
from pathlib import Path

def match_input(user_input, options, cutoff=0.6):
    return get_close_matches(user_input.lower(), options, n=1, cutoff=cutoff)

init(autoreset=True)

class Habit:
    def __init__(self, name, frequency, streak, last_completed):
        self.name = name
        self.frequency = frequency
        self.streak = streak
        self.last_completed = last_completed
    
    def marked_completed(self, today):  
        today = datetime.now()
        self.time_passed = today - last_completed # An error might occur beccause datetime and timedelta are being used together and both support different features.

        last_completed += 1
        self.reset_streak_if_needed()
        if self.streak == True:
            self.streak += 1                                 
            print(Fore.GREEN + f"You now have a {self.streak} {self.frequency} streak!")
        else:
            self.streak = 0
            print(Fore.RED + f"Your streak has been set to zero. Remember, consistency is key.")


    def reset_streak_if_needed(self, today):
        while True:
            frequencies = {
            'daily': timedelta(days=1),
            'weekly': timedelta(weeks=1),
            'monthly': relativedelta(months=1),
            'yearly': relativedelta(years=1)
            }

            self.frequency = frequencies.get(self.frequency.lower())

            if self.time_passed > timedelta(self.frequency):
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
    
class HabitTracker:
    def __init__(self, habits):
        self.habits = []

    def add_habit(self):
        while True:   
            habit_name = input("Please enter the name of the habit you would like to add: ").lower().strip()
            Habit.name = habit_name
            habit_freq = input("How frequently are you aiming to do your habit? Please type something along the lines of 'daily' or 'weekly': ")
            refined_freq = match_input(habit_freq, ['daily', 'weekly', 'monthly', 'yearly'])
            if refined_freq and refined_freq[0] == 'daily':
                habit = Habit(
                name=habit_name,
                frequency=refined_freq,
            )
                print(Fore.GREEN + "Your new task has been added successfully:")
                self.list_habit()
                if habit not in self.habits:
                    self.habits.append(habit)

            elif refined_freq and refined_freq[0] == 'weekly':
                habit = Habit(
                name=habit_name,
                frequency=refined_freq,
            )
                print(Fore.GREEN + "Your new task has been added successfully:")
                self.list_habit()
                if habit not in self.habits:
                    self.habits.append(habit)
            
            elif refined_freq and refined_freq[0] == 'yearly':
                habit = Habit(
                name=habit_name,
                frequency=refined_freq,
            )
                print(Fore.GREEN + "Your new task has been added successfully:")
                self.list_habit()
                if habit not in self.habits:
                    self.habits.append(habit)

            else:
                print(Fore.RED + f"Sorry, '{habit_freq}' does not seem to be a valid option, please try again.")
                continue

    def list_habits(self):
        if not self.habits:
            print(Fore.YELLOW + "You currently have no habits.")
            return
        print(Fore.GREEN + "Your list of tasks includes the following:")
        for habit in self.habits:
            print(f"- {habit.name} | Frequency: {habit.frequency} | "
            f"Streak: {habit.streak} | Last Completed: {habit.last_completed}")

    def mark_habit(self, index):
        while True:
            habit_marked = input("What task would you like to mark as done: ").strip().lower()
            for habit in self.habits:
                refined_habmar = match_input(habit_marked, [habit.name])
                if refined_habmar and refined_habmar[0] == habit.title:
                    Habit.marked_completed()
                    return
            print(Fore.RED + f"Sorry, '{habit_marked}' was not found in your list of habits.")
            continue
    
    def check_all_habits(self):
        for habit in self.habits:
            if Habit.time_passed > Habit.timedelta(self.frequency):        
                habit.streak = 0
            else:
                continue
    
    def save(self, filename):
        import storage
        path = Path("data") / f"{self.user_name}" / "habits.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        storage.save_tasks(self.habits, path)
        print(Fore.GREEN + f"Your habits have been saved, {self.user_name.capitalize()}")
        
    
    def load(self, filename):
        import storage
        path = Path("data") / f"{self.user_name}" / "habits.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        storage.load_tasks(self.habits, path)
        print(Fore.GREEN + f"Your habits have been loaded, {self.user_name.capitalize()}")
