from dateutil import parser
from datetime import datetime
from colorama import init, Fore
from difflib import get_close_matches
import re
import json
from pathlib import Path

def match_input(user_input, options, cutoff=0.6):
    return get_close_matches(user_input.lower(), options, n=1, cutoff=cutoff)

init(autoreset=True)

class User:
    def __init__(self, username, filename):
        self.username = username
        self.filename = filename
        self.task_manager = TaskManager(tasks=[], user_name=username)

    def return_file(self):
        path = Path("data") / f"{self.username}" / "tasks.json"
        return path

    def display_profile(self):
        print(Fore.GREEN + "Your profile summary includes the following:\n")
        print(f"Name - {self.username}\n"       
        f"Tasks - {self.task_manager.tasks}\n"
        f"Number of tasks - {len(self.task_manager.tasks)}\n"
        f"File name = {self.filename}")

class Task:
    def __init__(self, title, due_date, priority_level, status):
        self.title = title
        self.due_date = self.parse_strict_date(due_date)
        self.priority_level = priority_level
        self.status = status

    @staticmethod
    def parse_strict_date(date_str):
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date_str):
            raise ValueError("Date must be in the format YYYY-MM-DD (2025-07-08)")
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError as date:
            raise ValueError(Fore.RED + f"The date '{date}' is invalid.")

    def information_review(self):
        task_info = (f"Task title: {self.title} | Due Date: {self.due_date.strftime('%Y-%m-%d')}"
        f"| Priority Level: {self.priority_level} | Status: {self.status}").title()
        print(Fore.GREEN + "Your new task now includes the following info:\n"
              f"{task_info}")
    
    def status_update(self):
        while True:
            task_status = input("What would you like your task's status to be updated to?\n"
            "Please type in 'pending', 'done', or 'exit': ").strip()
            refined_task_status = match_input(task_status, ['pending', 'done', 'exit'])
            if refined_task_status and refined_task_status[0] == 'pending':
                self.status = 'pending'
                print(Fore.GREEN + f"Your task, '{self.title}' has been marked as pending.")
                break
            elif refined_task_status and refined_task_status[0] == 'done':
                self.status = 'done'
                print(Fore.GREEN + f"Your task, '{self.title}' has been marked as done.")
                break
            elif refined_task_status and refined_task_status[0] == 'exit':
                print("Okay. Going back to main menu...")
                break
            else:
                print(Fore.RED + f"Sorry, '{task_status}' is not a valid option, please try again.")
# These handle the creation of new tasks in storage.py and main.py:  
    def to_dict(self):
        return {
            'title': self.title,
            'due_date': self.due_date.isoformat(),
            'priority_level': self.priority_level,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data):
        due_date_obj = datetime.fromisoformat(data['due_date'])
        return cls(
            title=data['title'],
            due_date=due_date_obj.strftime('%Y-%m-%d'),
            priority_level=data['priority_level'],
            status=data['status']
        )
# -----------------------------------------------------------------
class TaskManager:
    def __init__(self, tasks, user_name):
        self.tasks = tasks if tasks is not None else []
        self.user_name = user_name
        
    def add_task(self, task=None):
        while True:
            new_task_title = input("What task do you want to add to your list of tasks: ").lower().strip()
            new_task_due_date = input("Please enter when your task is due(YYYY-MM-DD): ").lower().strip()
            try:
                Task.parse_strict_date(new_task_due_date)
            except ValueError:
                print(Fore.RED + f"Sorry, '{new_task_due_date}' is not in the format of (YYYY-MM-DD).")
                continue

            new_task_priority_level = input("Please enter your task's priority level on a scale from 0-5: ").strip()
      
            try:
                level = float(new_task_priority_level)
                if not (0 <= level <= 5):
                    print(Fore.RED + "Priority must be between 0 and 5.")
                    continue
            except ValueError:
                print(Fore.RED + f"Sorry, '{new_task_priority_level}' is not a valid number.")
                continue

            new_task_status = input("Please enter your task's status: ").lower().strip()
            refined_status = match_input(new_task_status, ['pending', 'done'])
            if not refined_status:
                print(Fore.RED + f"Invalid status '{new_task_status}'. Please enter 'pending' or 'done'.")
                continue

            task = Task(
                title=new_task_title,
                due_date=new_task_due_date,
                priority_level=level,
                status=refined_status[0]
            )

            print(Fore.GREEN + "Your new task has been added successfully:")
            task.information_review()
            if task not in self.tasks:
                self.tasks.append(task)
                break
            else:
                print(Fore.RED + f"Sorry, {task} seems to already be in your list.")

    def remove_task(self):
        while True:
            task_remove = input("Please enter the name of the task you would like to remove: ").lower().strip()
            matched = None
            for task in self.tasks:
                refined_removal = match_input(task_remove, [task.title])
                if refined_removal and refined_removal[0] == task.title:
                    matched = task
                    break
            if matched:
                self.tasks.remove(matched)
                print(Fore.GREEN + f"The task '{matched.title}' has been removed from your list of tasks.")
                break
            else:
                print(Fore.RED + f"Sorry, '{task_remove}' does not seem to be in your list of tasks.")
                continue

    def list_tasks(self):
        if not self.tasks:
            print(Fore.YELLOW + "You currently have no tasks.")
            return
        print(Fore.GREEN + "Your list of tasks includes the following:")
        for task in self.tasks:
            print(f"- {task.title} | Due: {task.due_date.strftime('%Y-%m-%d')} | "
            f"Priority: {task.priority_level} | Status: {task.status}")

    def mark_task(self):
        while True:
            user_mark = input("What task would you like to mark: ").strip().lower()
            for task in self.tasks:
                refined_mark = match_input(user_mark, [task.title])
                if refined_mark and refined_mark[0] == task.title:
                    task.status_update()
                    return
            print(Fore.RED + f"Sorry, '{user_mark}' was not found in your tasks.")
            continue

    def sort_tasks(self):
        while True:
            user_sort = input("How would you like to sort your tasks?\n"
            "Enter 'priority' to sort by importance or 'date' to sort by due date: ").strip()
            refined_sort = match_input(user_sort, ['priority', 'date'])

            if refined_sort and refined_sort[0] == 'priority':
                sorted_levels = sorted(self.tasks, key=lambda x: x.priority_level, reverse=True)
                print(Fore.GREEN + "Your sorted task list by priority:")
                for task in sorted_levels:
                    print(f"- {task.title} | Priority: {task.priority_level} | Due: {task.due_date.strftime('%Y-%m-%d')}")
                break

            elif refined_sort and refined_sort[0] == 'date':
                date_sorted_tasks = sorted(self.tasks, key=lambda x: x.due_date)
                print(Fore.GREEN + "Your sorted task list by due date:")
                for item in date_sorted_tasks:
                    print(f"- {item.title} | Due: {item.due_date.strftime('%Y-%m-%d')} | Priority: {item.priority_level}")
                break

            else:
                print(Fore.RED + f"'{user_sort}' is not a valid option, please try again.")

    def save_to_file(self):
        import storage
        path = Path("data") / f"{self.user_name}" / "tasks.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        storage.save_tasks(self.tasks, path)
        print(Fore.GREEN + f"Your tasks have been saved, {self.user_name.capitalize()}")
        
    def load_from_file(self):
        import storage
        path = Path("data") / f"{self.user_name}" / "tasks.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        storage.load_tasks(self.tasks, path)
        print(Fore.GREEN + f"Your tasks have been loaded, {self.user_name.capitalize()}")
        