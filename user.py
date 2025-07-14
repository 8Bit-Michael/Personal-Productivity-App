from colorama import init, Fore
from difflib import get_close_matches
from pathlib import Path
from task_manager import TaskManager
import json
import os
import storage

init(autoreset=True)

def match_input(user_input, options, cutoff=0.6):
    return get_close_matches(user_input.lower(), options, n=1, cutoff=cutoff)

class User:
    def __init__(self, username, filename):
        self.username = username
        self.filename = filename
        self.task_manager = TaskManager(tasks=[], user_name=username)

    def return_file(self):
        return Path("data") / self.username / "tasks.json"

    def display_profile(self):
        print(Fore.GREEN + "Your profile summary includes the following:\n")
        print(f"Name - {self.username}\n"       
              f"Tasks - {self.task_manager.tasks}\n"
              f"Number of tasks - {len(self.task_manager.tasks)}\n"
              f"File name = {self.filename}")

user = None

def create_new_user():
    global user
    name_input = input("Please enter your username: ").strip()
    username = name_input.title()

    path = Path("data") / username / "tasks.json"
    path.parent.mkdir(parents=True, exist_ok=True)

    user = User(username=username, filename=path)

    new_user_data = {
        "username": user.username,
        "filename": str(user.filename),
        "tasks": []
    }

    file_path = 'data/users.json'
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
        return None

    data.append(new_user_data)

    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

    with open(path, 'w') as f:
        json.dump([], f, indent=4)

    print(Fore.GREEN + f"User '{user.username}' created! Empty task file created at {path}")
    user.display_profile()
    return user.task_manager

def load_user():
    global user
    reload_name = input("Please enter your username: ").strip()
    username = reload_name.title()
    filename = Path("data") / username / "tasks.json"

    if filename.exists():
        print(Fore.GREEN + f"Welcome back, {username}!")
        loaded_tasks = storage.load_tasks(filename)
        user = User(username=username, filename=filename)
        user.task_manager = TaskManager(tasks=loaded_tasks, user_name=username)
        return user.task_manager
    else:
        print(Fore.RED + f"No data found for user '{username}'. Please create a new account first.")
        return None

def get_user_file():
    global user
    path = Path("data") / user.username / "tasks.json"
    return path.exists()

