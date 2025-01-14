from config import db

def get_all_books():
    return list(db.books.find())

def add_book(title, author):
    book = {"title": title, "author": author, "issued": False}
    db.books.insert_one(book)

def delete_book(title):
    db.books.delete_one({"title": title})

def issue_book(title, usn):
    book = db.books.find_one({"title": title})
    if book and not book['issued']:
        db.books.update_one({"title": title}, {"$set": {"issued": True, "issued_to": usn}})
        return True
    return False

def return_book(title):
    book = db.books.find_one({"title": title, "issued": True})
    if book:
        db.books.update_one({"title": title}, {"$set": {"issued": False, "issued_to": None}})
        return True
    return False

def get_issued_books():
    
    return list(db.books.find({"issued": True}))