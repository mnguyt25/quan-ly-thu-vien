import sqlite3

def get_db():
    return sqlite3.connect('library.db')

def show_books():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, title, author FROM books")
    books = cursor.fetchall()
    print("\nDanh sách sách:")
    for b in books:
        print(f"{b[0]}. {b[1]} - {b[2]}")
    db.close()

def search_books():
    keyword = input("Nhập từ khóa tìm kiếm: ")
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, title, author FROM books WHERE title LIKE ? OR author LIKE ?", 
                   (f"%{keyword}%", f"%{keyword}%"))
    books = cursor.fetchall()
    print("\nKết quả tìm kiếm:")
    for b in books:
        print(f"{b[0]}. {b[1]} - {b[2]}")
    db.close()

def show_profile(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    print("\nThông tin cá nhân:")
    print(f"Tên: {user[0]}")
    print(f"Email: {user[1]}")
    db.close()

def show_borrow_history(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT b.title, br.borrow_date, br.return_date
        FROM borrow_records br
        JOIN books b ON br.book_id = b.id
        WHERE br.user_id = ?
    """, (user_id,))
    records = cursor.fetchall()
    print("\nLịch sử mượn sách:")
    for r in records:
        print(f"{r[0]} - Ngày mượn: {r[1]} - Ngày trả: {r[2] if r[2] else 'Chưa trả'}")
    db.close()

def main():
    user_id = int(input("Nhập ID người dùng: "))
    while True:
        print("\n--- MENU ---")
        print("1. Xem danh sách sách")
        print("2. Tìm kiếm sách")
        print("3. Xem thông tin cá nhân")
        print("4. Xem lịch sử mượn sách")
        print("0. Thoát")
        choice = input("Chọn chức năng: ")
        if choice == '1':
            show_books()
        elif choice == '2':
            search_books()
        elif choice == '3':
            show_profile(user_id)
        elif choice == '4':
            show_borrow_history(user_id)
        elif choice == '0':
            break
        else:
            print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main() 