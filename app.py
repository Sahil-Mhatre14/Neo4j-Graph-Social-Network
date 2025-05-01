from models.user import register_user, login_user
from utils.interface import *

# Define main menu
main_menu = InterfaceMenu("Social Network", {
    "1": InterfaceOption("Register", register_user),
    "2": InterfaceOption("Login", login_user),
    "3": InterfaceOption("Quit", quit)
})

if __name__ == "__main__":
    main_menu.display()
