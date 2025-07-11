import json
from task_manager import Task
from colorama import init, Fore

init(autoreset=True)

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
            existing_keys.add(key)
    
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
        print(Fore.GREEN + "Your loaded tasks include the following:")
        for task in loaded_tasks:
            print(f"- {task.title} | Due: {task.due_date.strftime('%Y-%m-%d')} | Priority: {task.priority_level} | Status: {task.status}")
        return loaded_tasks
    except FileNotFoundError:
        print(Fore.RED + "Sorry, no task file has been detected.")
        return []
    except json.JSONDecodeError:
        print(Fore.RED + "Sorry, an error has occurred while the file was being read.")
        return []