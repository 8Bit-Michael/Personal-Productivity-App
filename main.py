from task_manager import Task, TaskManager
from colorama import init, Fore
from difflib import get_close_matches
import user

init(autoreset=True)

def match_input(user_input, options, cutoff=0.6):
    return get_close_matches(user_input.lower(), options, n=1, cutoff=cutoff)

if __name__ == '__main__':
    while True:
        manager = TaskManager(tasks=[], user_name='')
        login_data = input(
            "Welcome to my task manager app, to start please type in one of the following numbers:\n"
            "\n"
            "1. Log in.\n"
            "2. Create new account.\n"
            "3. Exit.\n"
        )

        refined_login = match_input(login_data, ['1', '2', '3'])

        if refined_login and refined_login[0] == '1':
            user_data = user.load_user()
            if user_data is not None:
                manager.user_name = user_data.user_name
                manager.tasks = user_data.tasks
            else:
                print(Fore.RED + "Failed to load user data.")
                continue

        elif refined_login and refined_login[0] == '2':
            user_data = user.create_new_user()
            if user_data is not None:
                manager.user_name = user_data.user_name
                manager.tasks = []
                manager.list_tasks()
            else:
                print(Fore.RED + "Failed to create new user.")
                continue

        else:
            print(Fore.RED + f"Sorry, {login_data} is not a valid option.")

        while True:
            user_choice = input("Welcome to my task manager app!\n"
            "Would you like to 'add' a task, 'remove' a task, 'list' your tasks,\n"
            "'mark' a task, 'sort' your tasks,'save' your tasks, 'load' them, or 'exit': ")
            refined_user_choice = match_input(user_choice, ['add', 'remove', 'list', 'mark', 'sort', 'save', 'load', 'exit'])

            if refined_user_choice and refined_user_choice[0] == 'add':
                manager.add_task()

            elif refined_user_choice and refined_user_choice[0] == 'remove':
                manager.remove_task()

            elif refined_user_choice and refined_user_choice[0] == 'list':
                manager.list_tasks()

            elif refined_user_choice and refined_user_choice[0] == 'mark':
                manager.mark_task()

            elif refined_user_choice and refined_user_choice[0] == 'sort':
                manager.sort_tasks()

            elif refined_user_choice and refined_user_choice[0] == 'exit':
                print("Okay, exiting program...")
                exit()

            elif refined_user_choice and refined_user_choice[0] == 'save':
                manager.save_to_file()

            elif refined_user_choice and refined_user_choice[0] == 'load':
                manager.load_from_file()
                                    
            else:
                print(Fore.RED + f"Sorry, {user_choice} is not a valid option.")
                continue