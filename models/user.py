from db.db import graph

def register_user():
    name = input("Enter your name: ").strip()
    email = input("Enter your email: ").strip()
    username = input("Choose a username: ").strip()
    password = input("Choose a password: ").strip()

    existing_user = graph.evaluate("""
    MATCH (u:User {username: $username})
    RETURN u
    """, username=username)

    if existing_user:
        print("Username already exists. Please try a different username.")
        return

    graph.run("""
    CREATE (u:User {name: $name, email: $email, username: $username, password: $password})
    """, name=name, email=email, username=username, password=password)
    
    print(f"User '{username}' registered successfully!")

def login_user():
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    user = graph.evaluate("""
    MATCH (u:User {username: $username, password: $password})
    RETURN u
    """, username=username, password=password)

    if user:
        print(f"Welcome back, {username}!")
        return username
    else:
        print("Invalid credentials. Please try again.")
        return None

def view_profile(username):
    profile = graph.evaluate("""
    MATCH (u:User {username: $username})
    RETURN u
    """, username=username)

    if profile:
        print("\n--- Your Profile ---")
        profile_data = dict(profile)
        print(f"Name    : {profile_data.get('name', 'N/A')}")
        print(f"Email   : {profile_data.get('email', 'N/A')}")
        print(f"Username: {profile_data.get('username', 'N/A')}")
        print(f"Bio     : {profile_data.get('bio', 'No bio set.')}")
    else:
        print("Profile not found.")


def edit_profile(username):
    print("\n--- Edit Your Profile ---")
    new_name = input("Enter new name (leave blank to keep unchanged): ").strip()
    new_email = input("Enter new email (leave blank to keep unchanged): ").strip()
    new_bio = input("Enter new bio (leave blank to keep unchanged): ").strip()

    if new_name:
        graph.run("""
        MATCH (u:User {username: $username})
        SET u.name = $new_name
        """, username=username, new_name=new_name)

    if new_email:
        graph.run("""
        MATCH (u:User {username: $username})
        SET u.email = $new_email
        """, username=username, new_email=new_email)

    if new_bio:
        graph.run("""
        MATCH (u:User {username: $username})
        SET u.bio = $new_bio
        """, username=username, new_bio=new_bio)

    print("Profile updated successfully!")
