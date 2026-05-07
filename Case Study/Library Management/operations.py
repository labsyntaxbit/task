from models import Book, Issue, Reservation
from datetime import datetime, timedelta
import random

class LibraryOperations:
    def __init__(self, library):
        self.library = library

    def add_book(self):
        book_id = input("Book ID: ")
        title = input("Title: ")
        author = input("Author: ")
        genre = input("Genre: ")
        isbn = input("ISBN: ")
        price = float(input("Price: "))
        copies = int(input("Copies Available: "))
        book = Book(book_id, title, author, genre, isbn, price, copies)
        self.library.books.append(book)
        self.library.save_books()
        print("Book added!")

    def update_book(self):
        book_id = input("Book ID to update: ")
        book = next((b for b in self.library.books if b.book_id == book_id), None)
        if book:
            book.price = float(input("New Price: "))
            book.copies_available = int(input("New Copies: "))
            self.library.save_books()
            print("Book updated!")
        else:
            print("Book not found.")

    def delete_book(self):
        book_id = input("Book ID to delete: ")
        self.library.books = [b for b in self.library.books if b.book_id != book_id]
        self.library.save_books()
        print("Book deleted!")

    def search_books(self, query, by='title'):
        if by == 'title':
            return [b for b in self.library.books if query.lower() in b.title.lower()]
        elif by == 'author':
            return [b for b in self.library.books if query.lower() in b.author.lower()]
        elif by == 'genre':
            return [b for b in self.library.books if query.lower() in b.genre.lower()]

    def issue_book(self, member_id):
        book_id = input("Book ID to issue: ")
        book = next((b for b in self.library.books if b.book_id == book_id), None)
        if book and book.copies_available > 0:
            issue_id = f"ISS{random.randint(1000,9999)}"
            issue_date = datetime.now()
            due_date = issue_date + timedelta(days=14)
            issue = Issue(issue_id, member_id, book_id, issue_date, due_date)
            self.library.issues.append(issue)
            book.copies_available -= 1
            self.library.save_issues()
            self.library.save_books()
            print(f"Book issued! Issue ID: {issue_id}, Due: {due_date.date()}")
        else:
            print("Book not available.")

    def return_book(self, member_id):
        issue_id = input("Issue ID: ")
        issue = next((i for i in self.library.issues if i.issue_id == issue_id and i.member_id == member_id), None)
        if issue:
            return_date = datetime.now()
            overdue_days = max(0, (return_date - issue.due_date).days)
            fine = overdue_days * 2
            book = next((b for b in self.library.books if b.book_id == issue.book_id), None)
            if book:
                book.copies_available += 1
            self.library.issues.remove(issue)
            self.library.returns.append({
                'issue_id': issue_id,
                'return_date': return_date.isoformat(),
                'fine': fine
            })
            self.library.save_issues()
            self.library.save_books()
            self.library.save_returns()
            print(f"Book returned. Fine: Rs.{fine}")
        else:
            print("Issue not found.")

    def reserve_book(self, member_id):
        book_id = input("Book ID to reserve: ")
        reservation_id = f"RES{random.randint(1000,9999)}"
        reservation = Reservation(reservation_id, member_id, book_id, 'requested')
        self.library.reservations.append(reservation)
        self.library.save_reservations()
        print("Reservation made!")

    def generate_reports(self):
        total_issued = len(self.library.issues)
        total_members = len(self.library.members)
        most_borrowed = max(self.library.books, key=lambda b: sum(1 for i in self.library.issues if i.book_id == b.book_id), default=None)
        overdue = [i for i in self.library.issues if datetime.now() > i.due_date]
        fine_collected = sum(r['fine'] for r in self.library.returns)
        lost_books = []  # Placeholder
        top_member = max(self.library.members, key=lambda m: len(m.borrowing_history), default=None)

        print(f"Total Books Issued: {total_issued}")
        print(f"Total Members: {total_members}")
        print(f"Most Borrowed Book: {most_borrowed.title if most_borrowed else 'None'}")
        print(f"Overdue Books: {len(overdue)}")
        print(f"Fine Collected: Rs.{fine_collected}")
        print(f"Lost Books: {len(lost_books)}")
        print(f"Top Active Member: {top_member.name if top_member else 'None'}")