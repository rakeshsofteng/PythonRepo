## returning multiple values using function
# def get_user_info():
#     name = "Rakesh"
#     age = 28
#     location = "Kharar, PB, India"
#     return name, age, location  # Returns a tuple

# # Unpacking the returned values
# user_name, user_age, user_location = get_user_info()

# print(f"Name: {user_name}")
# print(f"Age: {user_age}")
# print(f"Location: {user_location}")




##
## returning multiple values using function- using LIST

# def get_scores():
#     return [85, 90, 78]

# scores = get_scores()
# print(scores[0], scores[1], scores[2])





##
## returning multiple values using function- using Dictionary

# def get_config():
#     data= {
#         "host": "codeconfig.blogspot.com",
#         "port": 8080,
#         "debug": True
#           }
#     return data

# config = get_config()
# print(config["host"], config["port"], config["debug"])








##
## returning multiple values using function- using namedtuple

from collections import namedtuple

# Define the User namedtuple
User = namedtuple("User", ["name", "age", "location"])

# Function that returns multiple users
def get_users():
    user1 = User("Rakesh", 28, "Kharar")
    user2 = User("Aman", 25, "Delhi")
    user3 = User("Mukesh", 30, "Mumbai")
    return [user1, user2, user3]  # Return a list of User objects

# Accessing the returned users
users = get_users()

# Print each user's details
for user in users:
    print(f"Name: {user.name}, Age: {user.age}, Location: {user.location}")
