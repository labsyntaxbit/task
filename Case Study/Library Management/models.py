import json
import os
from datetime import datetime, timedelta

DATA_DIR = 'data'

class Book:
    def __init__(self, book_id, title, author, genre, isbn, price, copies_available):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.genre = genre
        self.isbn = isbn
        self.price = price
        self.copies_available = copies_available

    def to_dict(self):
        return {
            'book_id': self.book_id,
            'title': self.title,
            'author': self.author,
            'genre': self.genre,
            'isbn': self.isbn,
            'price': self.price,
            'copies_available': self.copies_available
        }

class Member:
    def __init__(self, member_id, name, address, contact, password, borrowing_history=None):
        self.member_id = member_id
        self.name = name
        self.address = address
        self.contact = contact
        self.password = password
        self.borrowing_history = borrowing_history if borrowing_history else []

    def to_dict(self):
        return {
            'member_id': self.member_id,
            'name': self.name,
            'address': self.address,
            'contact': self.contact,
            'password': self.password,
            'borrowing_history': self.borrowing_history
        }

class Issue:
    def __init__(self, issue_id, member_id, book_id, issue_date, due_date):
        self.issue_id = issue_id
        self.member_id = member_id
        self.book_id = book_id
        self.issue_date = issue_date
        self.due_date = due_date

    def to_dict(self):
        return {
            'issue_id': self.issue_id,
            'member_id': self.member_id,
            'book_id': self.book_id,
            'issue_date': self.issue_date.isoformat(),
            'due_date': self.due_date.isoformat()
        }

class Reservation:
    def __init__(self, reservation_id, member_id, book_id, status):
        self.reservation_id = reservation_id
        self.member_id = member_id
        self.book_id = book_id
        self.status = status  # requested, confirmed, issued, cancelled

    def to_dict(self):
        return {
            'reservation_id': self.reservation_id,
            'member_id': self.member_id,
            'book_id': self.book_id,
            'status': self.status
        }

class Library:
    def __init__(self):
        self.books = self.load_books()
        self.members = self.load_members()
        self.issues = self.load_issues()
        self.reservations = self.load_reservations()
        self.returns = self.load_returns()
        self.users = self.load_users()

    def load_books(self):
        try:
            with open(os.path.join(DATA_DIR, 'books.json'), 'r') as f:
                data = json.load(f)
                return [Book(**b) for b in data]
        except FileNotFoundError:
            return []

    def save_books(self):
        with open(os.path.join(DATA_DIR, 'books.json'), 'w') as f:
            json.dump([b.to_dict() for b in self.books], f, indent=4)

    def load_members(self):
        try:
            with open(os.path.join(DATA_DIR, 'members.json'), 'r') as f:
                data = json.load(f)
                return [Member(**m) for m in data]
        except FileNotFoundError:
            return []

    def save_members(self):
        with open(os.path.join(DATA_DIR, 'members.json'), 'w') as f:
            json.dump([m.to_dict() for m in self.members], f, indent=4)

    def load_issues(self):
        try:
            with open(os.path.join(DATA_DIR, 'issues.json'), 'r') as f:
                data = json.load(f)
                for i in data:
                    i['issue_date'] = datetime.fromisoformat(i['issue_date'])
                    i['due_date'] = datetime.fromisoformat(i['due_date'])
                return [Issue(**i) for i in data]
        except FileNotFoundError:
            return []

    def save_issues(self):
        with open(os.path.join(DATA_DIR, 'issues.json'), 'w') as f:
            json.dump([i.to_dict() for i in self.issues], f, indent=4)

    def load_reservations(self):
        try:
            with open(os.path.join(DATA_DIR, 'reservations.json'), 'r') as f:
                data = json.load(f)
                return [Reservation(**r) for r in data]
        except FileNotFoundError:
            return []

    def save_reservations(self):
        with open(os.path.join(DATA_DIR, 'reservations.json'), 'w') as f:
            json.dump([r.to_dict() for r in self.reservations], f, indent=4)

    def load_returns(self):
        try:
            with open(os.path.join(DATA_DIR, 'returns.json'), 'r') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            return []

    def save_returns(self):
        with open(os.path.join(DATA_DIR, 'returns.json'), 'w') as f:
            json.dump(self.returns, f, indent=4)

    def load_users(self):
        try:
            with open(os.path.join(DATA_DIR, 'users.json'), 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_users(self):
        with open(os.path.join(DATA_DIR, 'users.json'), 'w') as f:
            json.dump(self.users, f, indent=4)