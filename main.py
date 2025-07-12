from task_manager import Task, TaskManager
from colorama import init, Fore
from difflib import get_close_matches
import user
from habit_tracker import Habit, HabitTracker

init(autoreset=True)

def match_input(user_input, options, cutoff=0.6):
    return get_close_matches(user_input.lower(), options, n=1, cutoff=cutoff)

if __name__ == '__main__':
    # The sign-in options:
    while True:
        manager = TaskManager(tasks=[], user_name='')
        habit = HabitTracker(habits=[])
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
        # The main menu options:
        while True:
            user_choice = input("Welcome to my task manager app!\n"
            "Please choose one of the following to do using it's number:\n"
            "\n"
            "1. Use the habit tracker.\n"
            "2. Add tasks.\n"
            "3. List tasks.\n"
            "4. Remove task.\n"
            "5. Mark task as done.\n"
            "6. Sort tasks.\n"
            "7. Save task.\n"
            "8. Load task.\n"
            "9. Exit\n")
            refined_user_choice = match_input(user_choice, ['1', '2', '3', '4', '5', '6', '7', '8', '9'])
            if refined_user_choice and refined_user_choice[0] == '1':
                # The habit options:
                while True:
                    habit_choice = input("Welcome to the habit manager! Please choose one of the following to do:\n"
                    "1. View habits.\n" 
                    "2. Add habit.\n"
                    "3. Mark habit as complete.\n"
                    "4. Back")
                    refined_user_choice = match_input(habit_choice, ['1', '2', '3', '4'])
                    if refined_user_choice and refined_user_choice[0] == '1':
                        habit.list_habits()

                    elif refined_user_choice and refined_user_choice[0] == '2':
                        habit.add_habit()

                    elif refined_user_choice and refined_user_choice[0] == '3':
                        habit.mark_habit()

                    elif refined_user_choice and refined_user_choice[0] == '4':
                        break
                                            
                    else:
                        print(Fore.RED + f"Sorry, {habit_choice} is not a valid option.")
                        continue

            elif refined_user_choice and refined_user_choice[0] == '2':
                manager.add_task()

            elif refined_user_choice and refined_user_choice[0] == '3':
                manager.list_tasks()

            elif refined_user_choice and refined_user_choice[0] == '4':
                manager.remove_task()

            elif refined_user_choice and refined_user_choice[0] == '5':
                manager.mark_task()
        
            elif refined_user_choice and refined_user_choice[0] == '6':
                manager.sort_tasks()
     
            elif refined_user_choice and refined_user_choice[0] == '7':
                manager.save_to_file()
        
            elif refined_user_choice and refined_user_choice[0] == '8':
                manager.load_from_file()

            elif refined_user_choice and refined_user_choice[0] == '9':
                print("Okay, goodbye!")
                exit()
                                    
            else:
                print(Fore.RED + f"Sorry, {user_choice} is not a valid option.")
                continue
