from colorama import init, Fore
from difflib import get_close_matches
from pathlib import Path
from task_manager import User
import json
import os

init(autoreset=True)

def match_input(user_input, options, cutoff=0.6):
    return get_close_matches(user_input.lower(), options, n=1, cutoff=cutoff)

user = User(username='', filename='')

def create_new_user():
    name_input = input("Please enter your username: ").strip()
    user.username = name_input.title()  # Use title case for nicer usernames

    # Create directory and tasks.json path:
    path = Path("data") / user.username / "tasks.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    user.filename = path

    from task_manager import TaskManager
    user.task_manager = TaskManager(tasks=[], user_name=user.username)

    # Save the user info to users.json:
    new_user = {
        "username": user.username,
        "filename": str(user.filename),
        "tasks": []
    }

    file_path = 'data/users.json' # Here's what's not saving the data to users.json.
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    if any(u['username'] == user.username for u in data):
        print(Fore.YELLOW + f"User '{user.username}' already exists. Please log in instead.")
        return

    data.append(new_user)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    with open(path, 'w') as f:
        json.dump([], f, indent=4)

    print(Fore.GREEN + f"User '{user.username}' created! Empty task file created at {path}")
    user.display_profile()

def load_user():
    from task_manager import TaskManager
    import storage

    reload_name = input("Please enter your username: ").strip()
    user.username = reload_name.title()
    user.filename = Path("data") / user.username / "tasks.json"

    if user.filename.exists():
        print(Fore.GREEN + f"Welcome back, {user.username}!")

        # Load tasks from the user's file:
        loaded_tasks = storage.load_tasks(user.filename)

        # Initialize TaskManager with loaded tasks:
        user.task_manager = TaskManager(tasks=loaded_tasks, user_name=user.username)
        user.task_manager.list_tasks()
        return user.task_manager
    else:
        print(Fore.RED + f"No data found for user '{user.username}'. Please create a new account first.")
        return None

def get_user_file():
    path = Path("data") / user.username / "tasks.json"
    return path.exists()
