import getpass
from models import Library

class AuthSystem:
    def __init__(self, library):
        self.library = library
        self.failed_attempts = {}

    def login(self):
        username = input("Username: ")
        password = input("Password: ")
        if username in self.library.users:
            if self.library.users[username]['password'] == password:
                print("Login successful!")
                self.failed_attempts[username] = 0
                return username, self.library.users[username]['role']
            else:
                self.failed_attempts[username] = self.failed_attempts.get(username, 0) + 1
                if self.failed_attempts[username] >= 3:
                    print("Account locked due to 3 failed attempts.")
                    return None, None
                print("Invalid password.")
        else:
            print("User not found.")
        return None, None

    def register_member(self):
        member_id = input("Member ID: ")
        name = input("Name: ")
        address = input("Address: ")
        contact = input("Contact: ")
        password = input("Password: ")
        member = Member(member_id, name, address, contact, password)
        self.library.members.append(member)
        self.library.users[member_id] = {'password': password, 'role': 'member'}
        self.library.save_members()
        self.library.save_users()
        print("Member registered successfully!")

from models import Member