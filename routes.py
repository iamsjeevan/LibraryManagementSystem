from flask import Flask, render_template, request, redirect, url_for, flash
from models import get_all_books, add_book, delete_book, issue_book, return_book, get_issued_books

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # For flash messages

@app.route('/')
def index():
    search_query = request.args.get('search', '')
    filtered_books = [book for book in get_all_books() if search_query.lower() in book['title'].lower()]
    return render_template('index.html', books=filtered_books, search_query=search_query)

@app.route('/add-book', methods=['POST'])
def add_book_route():
    title = request.form['title']
    author = request.form['author']
    add_book(title, author)
    flash('Book added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/delete-book/<title>', methods=['POST'])
def delete_book_route(title):
    delete_book(title)
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/issue-book', methods=['GET', 'POST'])
def issue_book_route():
    if request.method == 'POST':
        title = request.form.get('issue-title', '').strip()
        usn = request.form.get('usn', '').strip()
        if not title or not usn:
            flash('Invalid input. Please provide both Title and USN.', 'error')
        else:
            result = issue_book(title, usn)
            if result:
                flash('Book issued successfully!', 'success')
            else:
                flash('Failed to issue book. It may already be issued.', 'error')
        return redirect(url_for('issue_book_route'))

    # Pass all books to the template for the dropdown
    books = get_all_books()
    return render_template('issue-book.html', books=books)


@app.route('/return-book', methods=['POST'])
def return_book_route():
    title = request.form['return-title']
    result = return_book(title)
    if result:
        flash('Book returned successfully!', 'success')
    else:
        flash('Failed to return book. It may not have been issued.', 'error')
    return redirect(url_for('index'))

@app.route('/issued-books')
def issued_books_route():
    issued_books_list = get_issued_books()
    return render_template('issued-books.html', issued_books=issued_books_list)

if __name__ == '__main__':
    app.run(debug=True)
