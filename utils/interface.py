from models import user
import os

def cls(last_message=None):
    os.system('cls' if os.name == 'nt' else 'clear')
    if last_message:
        print(last_message)

class InterfaceOption:
    def __init__(self, display_text, callback, custom_display=None):
        self.display_text = display_text
        self.callback = callback
        self.custom_display = custom_display

    def call(self, *args, **kwargs):
        if args or kwargs:
            self.callback(*args, **kwargs)
        else:
            self.callback()

class InterfaceMenu:
    def __init__(self, title, options: dict[InterfaceOption]):
        self.title = title
        self.options = options
        cls()

    def display(self):
        """Show the menu"""
        print(f"--- {self.title} ---")
        for option in self.options:
            if self.options[option].custom_display:
                print(self.options[option].custom_display)
            else:
                print(f"[{option}] {self.options[option].display_text}")

        command = self.get_input()
        command.call()
        return self.display()

    def get_input(self, free_input=False) -> InterfaceOption:
        if free_input:
            return input("").strip()
        
        option = None

        while not option:
            choice = input("Enter selection: ").strip()
            
            try:
                option = self.options[choice]
            except:
                option = None
                print(f"{choice} is not a valid option.")
        
        return option

class UserMenu(InterfaceMenu):
    def __init__(self, username):
        self.username = username
        self.title = f"Welcome {username}!"
        cls()
    
    def display(self):
        print(f"--- {self.title} ---")
        print("[1] View Profile")
        print("[2] Edit Profile")
        print("[3] Search Users")
        print("[4] Friend Recommendations")
        print("[5] Popular Users")
        print("[6] Logout")

        command = input("Enter selection: ").strip()
        if command == "1":
            UserInteractionMenu(self.username).display()
        elif command == "2":
            user.edit_profile(self.username)
        elif command == "3":
            query = input("Enter the name of the user you are searching for: ")
            cls("--- User Search ---")
            print(f"Searching for {query}...")
            result = user.search_users(query)
            if result:
                UserInteractionMenu(self.username, result).display()
            else:
                cls("User not found. Try searching again")
        elif command == "4":
            # TODO
            pass
        elif command == "5":
            n = input("Enter number of users to search for (leave blank for default 10): ")
            try:
                n = int(n)
            except:
                n = 10

            if n <= 0:
                n = 10

            cls(f"--- Top {n} Most Popular Users ---")
            result = user.popular_users(n)
            if result:
                UserInteractionMenu(self.username, result).display()
            else:
                cls("Invalid user selection.")
        elif command == "6":
            cls(f"Logged out of {self.username}")
            return
        else:
            cls(f"{command} is not a valid option.")
        
        return self.display()

class UserInteractionMenu(InterfaceMenu):
    def __init__(self, own_username, other_user=None):
        self.own_username = own_username
        self.other_user = other_user
        self.options = {}
        cls()

        # if other_user is unset we use the user
        if not self.other_user:
            self.other_user = user.get_profile(own_username)

        if self.own_username != self.other_user.get('username'):
            following_other = user.check_following(own_username, other_user.get('username'))
            other_follows = user.check_following(other_user.get('username'), own_username)

            if other_follows:
                self.options['0'] = InterfaceOption("Remove Follower", self.remove_follower)

            if following_other:
                self.options['1'] = InterfaceOption("Unfollow", self.unfollow)
            else:
                self.options['1'] = InterfaceOption("Follow", self.follow)

        self.options['2'] = InterfaceOption("View Followers", self.view_followers)
        self.options['3'] = InterfaceOption("View Following", self.view_following)
        
        if self.own_username != self.other_user.get('username'):
            self.options['4'] = InterfaceOption("View Mutual Connections", self.view_mutuals)
        
        self.options['5'] = InterfaceOption("Exit Profile", self.exit)


    def display(self):
        self.followers = user.get_followers(self.other_user.get('username'))
        self.following = user.get_following(self.other_user.get('username'))

        if len(self.followers) == 0 and self.options.get('2'):
            del self.options['2']
            
        if len(self.following) == 0 and self.options.get('3'):
            del self.options['3']

        print(f"--- Viewing Profile ---")
        print(f"Name     : {self.other_user.get('name', 'N/A')}")
        print(f"Email    : {self.other_user.get('email', 'N/A')}")
        print(f"Username : {self.other_user.get('username', 'N/A')}")
        print(f"Bio      : {self.other_user.get('bio', 'No bio set.')}")
        print(f"Followers: {len(self.followers)}")
        print(f"Following: {len(self.following)}")
        print("")
        for option in self.options:
            print(f"[{option}] {self.options[option].display_text}")

        command = self.get_input()
        command.call()

    def unfollow(self):
        user.remove_follower(self.own_username, self.other_user.get('username'))
        self.options['1'] = InterfaceOption("Follow", self.follow)
        return self.display()

    def follow(self):
        user.add_follower(self.own_username, self.other_user.get('username'))
        self.options['1'] = InterfaceOption("Unfollow", self.unfollow)
        return self.display()

    def remove_follower(self):
        user.remove_follower(self.other_user.get('username'), self.own_username)
        del self.options['0']
        return self.display()

    def view_followers(self):
        if not self.followers:
            cls("No users returned.")
            return self.display()
        
        cls(f"--- Followers of {self.other_user.get('username')} ---")
        print("Select a user from the following list: ")
        for i in range(len(self.followers)):
            user = self.followers[i][0]
            print(f"[{i+1}] {user.get('name')} ({user.get('username')})")
        
        choice = input("Enter selection: ").strip()

        try:
            choice = int(choice)
            if choice < 1 or choice > len(self.followers):
                raise Exception
        except:
            cls("Invalid selection.")
        else:   
            user_choice = self.followers[int(choice)][0]
            UserInteractionMenu(self.own_username, user_choice).display()
        return self.display()

    def view_following(self):
        if not self.following:
            cls("No users returned.")
            return self.display()
        
        cls(f"--- Users that {self.other_user.get('username')} follows ---")
        print("Select a user from the following list: ")
        for i in range(len(self.following)):
            user = self.following[i][0]
            print(f"[{i}] {user.get('name')} ({user.get('username')})")
        
        choice = input("Enter selection: ").strip()

        try:
            choice = int(choice)
            if choice < 1 or choice > len(self.following):
                raise Exception
        except:
            cls("Invalid selection.")
        else:   
            user_choice = self.following[int(choice)][0]
            UserInteractionMenu(self.own_username, user_choice).display()
        return self.display()

    def view_mutuals(self):
        cls(f"--- Users followed by {self.own_username} and {self.other_user.get('username')} ---")
        mutuals = user.get_mutuals(self.own_username, self.other_user.get('username'))
        
        if not mutuals:
            cls(f"You have no mutual connections with {self.other_user.get('username')}")
            return self.display()

        for i in range(len(mutuals)):
            mutual = mutuals[i][0]
            print(f"[{i}] {mutual.get('name')} ({mutual.get('username')})")

        choice = input("Enter selection: ").strip()

        try:
            choice = int(choice)
            if choice < 1 or choice > len(mutuals):
                raise Exception
        except:
            cls("Invalid selection.")
        else:   
            user_choice = mutuals[int(choice)][0]
            UserInteractionMenu(self.own_username, user_choice).display()
        return self.display()

    def exit(self):
        cls()
        return