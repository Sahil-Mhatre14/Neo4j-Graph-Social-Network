from models.user import register_user, login_user, view_profile, edit_profile

def main_menu():
    print("\n--- Social Network ---")
    print("1. Register")
    print("2. Login")
    print("3. Exit")
    choice = input("Choose an option: ")
    return choice

def user_menu(username):
    print(f"\n--- Welcome {username} ---")
    print("1. View Profile")
    print("2. Edit Profile")
    print("3. Logout")
    choice = input("Choose an option: ")
    return choice

def main():
    while True:
        choice = main_menu()

        if choice == '1':
            register_user()
        elif choice == '2':
            username = login_user()
            if username:
                while True:
                    user_choice = user_menu(username)
                    if user_choice == '1':
                        view_profile(username)
                    elif user_choice == '2':
                        edit_profile(username)
                    elif user_choice == '3':
                        print("Logging out...")
                        break
                    else:
                        print("Invalid choice. Try again.")
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
