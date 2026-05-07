from models import Library
from auth import AuthSystem
from operations import LibraryOperations

def main():
    library = Library()
    auth = AuthSystem(library)
    ops = LibraryOperations(library)

    current_user = None
    role = None

    while True:
        if not current_user:
            print("\n1. Login")
            print("2. Register Member")
            print("11. Exit")
            choice = input("Choose: ")
            if choice == '1':
                current_user, role = auth.login()
            elif choice == '2':
                auth.register_member()
            elif choice == '11':
                break
            else:
                print("Invalid choice.")
        else:
            print(f"\nLogged in as {current_user} ({role})")
            if role == 'librarian':
                print("1. Add Book")
                print("2. Update Book")
                print("3. Delete Book")
                print("4. Search Books")
                print("5. View All Books")
                print("6. Reports")
                print("10. Logout")
            else:
                print("1. Search Books")
                print("2. View All Books")
                print("3. Issue Book")
                print("4. Return Book")
                print("5. Reserve Book")
                print("6. View Profile")
                print("10. Logout")
            print("11. Exit")
            choice = input("Choose: ")
            if choice == '1' and role == 'librarian':
                ops.add_book()
            elif choice == '2' and role == 'librarian':
                ops.update_book()
            elif choice == '3' and role == 'librarian':
                ops.delete_book()
            elif choice == '3' and role == 'member':
                ops.issue_book(current_user)
            elif choice == '4' and role == 'member':
                ops.return_book(current_user)
            elif choice == '5' and role == 'member':
                ops.reserve_book(current_user)
            elif choice == '6' and role == 'member':
                member = next((m for m in library.members if m.member_id == current_user), None)
                if member:
                    print(f"Name: {member.name}, Address: {member.address}, Contact: {member.contact}")
                    print("Borrowing History:", member.borrowing_history)
            elif choice == '4':
                query = input("Search query: ")
                by = input("By (title/author/genre): ")
                results = ops.search_books(query, by)
                for b in results:
                    print(f"{b.book_id}: {b.title} by {b.author}")
            elif choice == '5':
                for b in library.books:
                    print(f"{b.book_id}: {b.title} by {b.author} - {b.copies_available} copies")
            elif choice == '6' and role == 'librarian':
                ops.generate_reports()
            elif choice == '10':
                current_user = None
                role = None
            elif choice == '11':
                break
            else:
                print("Invalid choice.")

if __name__ == '__main__':
    main()