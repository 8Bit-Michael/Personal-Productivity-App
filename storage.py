import json
from colorama import Fore
from task_manager import Task
from habit_tracker import Habit

def save_tasks(task_list, filename):
    # This is a one liner which uses each task in the task list to run to_dict()
    #  if it's an instance of the Task class:
    new_tasks = [task.to_dict() for task in task_list if isinstance(task, Task)]

    try:
        # This tries to open the file, but checks if there's an instance of a list with actual tasks in them.
        # So if there is not, an error comes up, and the program handles that by creating a new list to store
        # the tasks in the .JSON file.
        with open(filename, 'r') as file:
            existing_tasks = json.load(file)
            if not isinstance(existing_tasks, list):
                existing_tasks = []
    except (FileNotFoundError, json.JSONDecodeError):
        existing_tasks = []
    
    # This keeps track of each unique key in the .JSON file:
    existing_keys = {(task['title'], task['due_date']) for task in existing_tasks}

    # This only appends tasks that don't exist in the .JSON file to the .JSON to avoid duplications:
    for task in new_tasks:
        key = (task['title'], task['due_date'])
        if key not in existing_keys:
            existing_tasks.append(task)

    with open(filename, 'w') as file:
        json.dump(existing_tasks, file, indent=4)

def load_tasks(filename):
    try:
        # This takes info from the .json file:
        with open(filename, 'r') as file:
            tasks_dict = json.load(file)
            # This adds each task to a list:
            loaded_tasks = [Task.from_dict(task_dict) for task_dict in tasks_dict]
          # This gives some output and sends outputs if errors happen:
        print(Fore.GREEN + "Tasks loaded:")
        for task in loaded_tasks:
            print(f"- {task.title} | Due: {task.due_date.strftime('%Y-%m-%d')} | Priority: {task.priority_level} | Status: {task.status}")
        return loaded_tasks
    except FileNotFoundError:
        print(Fore.RED + "No task file found.")
        return []
    except json.JSONDecodeError:
        print(Fore.RED + "Error reading task file.")
        return []

def save_habits(habits, filename):
    new_habits = [habit.to_dict() for habit in habits if isinstance(habit, Habit)]

    try:
        with open(filename, 'r') as file:
            existing_habits = json.load(file)
            if not isinstance(existing_habits, list):
                existing_habits = []
    except (FileNotFoundError, json.JSONDecodeError):
        existing_habits = []

    existing_keys = {(h['name'], h['frequency']) for h in existing_habits}
    for habit in new_habits:
        key = (habit['name'], habit['frequency'])
        if key not in existing_keys:
            existing_habits.append(habit)

    with open(filename, 'w') as file:
        json.dump(existing_habits, file, indent=4)

def load_habits(filename):
    try:
        with open(filename, 'r') as file:
            habits_dict = json.load(file)
            loaded_habits = [Habit.from_dict(h) for h in habits_dict]
        print(Fore.GREEN + "Habits loaded:")
        for h in loaded_habits:
            print(f"- {h.name} | Frequency: {h.frequency} | Last Completed: {h.last_completed} | Streak: {h.streak}")
        return loaded_habits
    except FileNotFoundError:
        print(Fore.RED + "No habit file found.")
        return []
    except json.JSONDecodeError:
        print(Fore.RED + "Error reading habit file.")
        return []
