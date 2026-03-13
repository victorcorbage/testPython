import os
import platform


def clear_screen():
    os.system('cls' if platform.system() == 'Windows' else 'clear')


def print_header(text):
    print("\n" + "=" * 50)
    print(f"  {text}")
    print("=" * 50)


def get_user_input(prompt):
    return input(prompt).strip()


def validate_priority(priority):
    valid_priorities = ["low", "medium", "high"]
    return priority.lower() in valid_priorities


def format_datetime(dt_string):
    try:
        dt = datetime.strptime(dt_string, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%b %d, %Y at %I:%M %p")
    except:
        return dt_string
