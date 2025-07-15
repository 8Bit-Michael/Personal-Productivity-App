from task_manager import TaskManager
from colorama import init, Fore
from difflib import get_close_matches
import user
from habit_tracker import HabitTracker
from calendar_events import Calendar

init(autoreset=True)

def match_input(user_input, options, cutoff=0.6):
    return get_close_matches(user_input.lower(), options, n=1, cutoff=cutoff)

if __name__ == '__main__':
    while True:
        manager = TaskManager(tasks=[], user_name='')
        habit = HabitTracker(habits=[])
        calendar = Calendar()

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
            if user_data and hasattr(user_data, 'user_name') and hasattr(user_data, 'tasks'):
                manager.user_name = user_data.user_name
                manager.tasks = user_data.tasks
            else:
                print(Fore.RED + "Failed to load user data. Please try again or create a new account.")
                continue

        elif refined_login and refined_login[0] == '2':
            user_data = user.create_new_user()
            if user_data and hasattr(user_data, 'user_name') and hasattr(user_data, 'tasks'):
                manager.user_name = user_data.user_name
                manager.tasks = user_data.tasks
                manager.list_tasks()
            else:
                print(Fore.RED + "Failed to create new user. Please try again.")
                continue

        elif refined_login and refined_login[0] == '3':
            print("Okay, goodbye!")
            raise RuntimeError("Exited program.")
        
        else:
            print(Fore.RED + f"Sorry, '{login_data}' is not a valid option.")
            continue

        # Main menu
        while True:
            user_choice = input("Welcome to my task manager app!\n"
            "Please choose one of the following to do using its number:\n"
            "\n"
            "1. Use the habit tracker.\n"
            "2. Add tasks.\n"
            "3. List tasks.\n"
            "4. Remove task.\n"
            "5. Mark task as done.\n"
            "6. Sort tasks.\n"
            "7. Save task.\n"
            "8. Load task.\n"
            "9. Calendar & Events.\n"
            "10. Exit\n")

            refined_user_choice = match_input(user_choice, ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'])

            if refined_user_choice and refined_user_choice[0] == '1':
                while True:
                    habit_choice = input("Welcome to the habit manager! Please choose one of the following:\n"
                        "1. View habits.\n" 
                        "2. Add habit.\n"
                        "3. Mark habit as complete.\n"
                        "4. Save habit.\n"
                        "5. Load habit.\n"
                        "6. Back\n")

                    refined_habit_choice = match_input(habit_choice, ['1', '2', '3', '4', '5', '6'])

                    if refined_habit_choice and refined_habit_choice[0] == '1':
                        habit.list_habits()
                    elif refined_habit_choice and refined_habit_choice[0] == '2':
                        habit.add_habit()
                    elif refined_habit_choice and refined_habit_choice[0] == '3':
                        habit.mark_habit()
                    elif refined_habit_choice and refined_habit_choice[0] == '4':
                        habit.save(username=user_data.user_name)
                    elif refined_habit_choice and refined_habit_choice[0] == '5':
                        habit.load(username=user_data.user_name)
                    elif refined_habit_choice and refined_habit_choice[0] == '6':
                        break
                    else:
                        print(Fore.RED + f"Sorry, '{habit_choice}' is not a valid option.")
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
                while True:
                    events_choice = input("Welcome to the events manager! Please choose one of the following:\n"
                        "1. View events.\n" 
                        "2. Add event.\n"
                        "3. Get upcoming events.\n"
                        "4. Save event.\n"
                        "5. Load event.\n"
                        "6. Back\n")

                    refined_event_choice = match_input(events_choice, ['1', '2', '3', '4', '5', '6'])

                    if refined_event_choice and refined_event_choice[0] == '1':
                        calendar.list_events()
                    elif refined_event_choice and refined_event_choice[0] == '2':
                        calendar.add_event()
                    elif refined_event_choice and refined_event_choice[0] == '3':
                        calendar.get_upcoming_events()
                    elif refined_event_choice and refined_event_choice[0] == '4':
                        calendar.save(username=user_data.user_name)
                    elif refined_event_choice and refined_event_choice[0] == '5':
                        calendar.load(username=user_data.user_name)
                    elif refined_event_choice and refined_event_choice[0] == '6':
                        break
                    else:
                        print(Fore.RED + f"Sorry, '{events_choice}' is not a valid option.")
                        continue

            elif refined_user_choice and refined_user_choice[0] == '10':
                print("Okay, goodbye!")
                raise RuntimeError("Exited program.")
            
            else:
                print(Fore.RED + f"Sorry, '{user_choice}' is not a valid option.")
                continue
