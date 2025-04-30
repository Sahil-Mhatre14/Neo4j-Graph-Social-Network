from db.db import graph
from utils.interface import UserMenu, cls

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
        UserMenu(username).display()
    else:
        print("Invalid credentials. Please try again.")
        return None

def get_followers(username):
    followers = graph.run("""
    MATCH (u:User {username: $username})<-[:FOLLOWS]-(follower:User)
    RETURN follower
    """, username=username)

    return list(followers) if followers else []

def get_following(username):
    following = graph.run("""
    MATCH (u:User {username: $username})-[:FOLLOWS]->(following:User)
    RETURN following
    """, username=username)

    return list(following) if following else []

def check_following(follower, followed):
    following = graph.evaluate("RETURN EXISTS( (:User {username: $follower})-[:FOLLOWS]->(:User {username: $followed}) )", follower=follower, followed=followed)
    return following

def get_profile(username):
    profile = graph.evaluate("""
    MATCH (u:User {username: $username})
    RETURN u
    """, username=username)

    return dict(profile)

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

def search_users(query):
    users = graph.run("""
    MATCH (u:User)
    WHERE u.username CONTAINS $name OR u.name CONTAINS $name       
    RETURN u
    """, name=query)

    users = list(users)

    if not users:
        return None
    
    print("Select a user from the following list: ")

    for i in range(len(users)):
        user = users[i][0]
        print(f"[{i+1}] {user.get('name')} ({user.get('username')})")

    choice = input("Enter selection: ")

    try:
        choice = int(choice)
        if choice < 1 or choice > len(users):
            return None
    except:
        return None
    
    user_choice = users[choice][0]

    return dict(user_choice)
    
def remove_follower(follower, followed):
    graph.run("""
    MATCH (:User {username: $follower})-[r:FOLLOWS]->(:User {username: $followed})
    DELETE r""", follower=follower, followed=followed)

def add_follower(follower, followed):
    graph.run("""
    MATCH (follower:User {username: $follower}), (followed:User {username: $followed})
    CREATE (follower)-[:FOLLOWS]->(followed)
    """, follower=follower, followed=followed)

def get_mutuals(user1, user2):
    """Returns all users that are followed by both user1 and user2"""
    query = """
            MATCH (a:User {username: $user1})-[:FOLLOWS]->(mutual:User)<-[:FOLLOWS]-(b:User {username: $user2})
            RETURN mutual"""
    
    mutuals = graph.run(query, user1=user1, user2=user2)
    return list(mutuals) if mutuals else []

def get_also_followed_by(user1, user2):
    """Returns all people that user1 follows that follow user2 (implementation of Instagram's "Also followed by" feature)"""
    
    query = """
            MATCH (a:User {username: $user1})-[:FOLLOWS]->(mutual:User)-[:FOLLOWS]->(b:User {username: $user2})
            RETURN mutual
            """
    also_followed_by = graph.run(query, user1=user1, user2=user2)
    return list(also_followed_by) if also_followed_by else []

def popular_users(n):
    users = graph.run("""
    MATCH (follower:User)-[:FOLLOWS]->(top:User)
    WITH top, COLLECT(follower) as followers
    RETURN top, SIZE(followers)
    ORDER BY SIZE(followers) DESC LIMIT $number
    """, number=int(n))

    users = list(users)

    if not users:
        return None
    
    print("Select a user from the following list: ")

    for i in range(len(users)):
        user = users[i]
        print(f"[{i+1}] {user[0].get('name')} ({user[0].get('username')}) - {user[1]} Followers")

    choice = input("Enter selection: ")

    try:
        choice = int(choice)
        if choice < 1 or choice > n:
            return None
    except:
        return None
    
    user_choice = users[choice][0]

    return dict(user_choice)