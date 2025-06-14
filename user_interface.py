import tkinter as tk
from tkinter import messagebox,  ttk, messagebox, simpledialog
import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="taolao",
    database="library_db"
)

cursor = conn.cursor()
cursor.execute("SHOW TABLES;")  # ví dụ kiểm tra kết nối
for x in cursor:
    print(x)

conn.close()


def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="taolao",
        database="library"
    )

# ======= Giao diện Người dùng =======
def open_user_interface (user_id):
    window = tk.Tk()
    window.title("Giao diện Người dùng")
    window.geometry("400x300")
    try:
        window.iconbitmap("books_icon.ico")
    except:
        pass
    
    # === Menu Bar ===
    menubar = tk.Menu(window)
    
    menubar.add_command(label="Mượn sách", command=borrow)
    
    menubar.add_command(label="Trả sách", command=return_book)
    
    menubar.add_command(label="Thoát", command=window.destroy)
    
    window.config(menu=menubar)
    
    tk.Label(window, text="Thư viện", font=("Arial", 16)).pack(pady=20)
    window.mainloop()

#tabs
    notebook = ttk.Notebook(window)
    notebook.pack(fill="both", expand=True)

# Tab 1: Danh sách sách
    tab_books = ttk.Frame(notebook)
    notebook.add(tab_books, text="Danh sách sách")
    tree_books = ttk.Treeview(tab_books, columns=("ID", "Tên sách", "Tác giả"), show="headings")
    for col in ("ID", "Tên sách", "Tác giả"):
        tree_books.heading(col, text=col)
        tree_books.column(col, width=200)
    tree_books.pack(fill="both", expand=True, padx=10, pady=10)
    load_books(tree_books)

# Tab 2 Tìm kiếm sách
    tab_search = ttk.Frame(notebook)
    notebook.add(tab_search, text="Tìm kiếm sách")
    frame_search = ttk.Frame(tab_search)
    frame_search.pack(pady=10)
    tk.Label(frame_search, text="Từ khóa:").pack(side="left")
    entry_search = tk.Entry(frame_search)
    entry_search.pack(side="left", padx=5)
    btn_search = tk.Button(frame_search, text="Tìm", command=lambda: search_books(entry_search.get(), tree_search))
    btn_search.pack(side="left")
    tree_search = ttk.Treeview(tab_search, columns=("ID", "Tên sách", "Tác giả"), show="headings")
    for col in ("ID", "Tên sách", "Tác giả"):
        tree_search.heading(col, text=col)
        tree_search.column(col, width=200)
    tree_search.pack(fill="both", expand=True, padx=10, pady=10)

 # Tab 3: Thông tin cá nhân
    tab_profile = ttk.Frame(notebook)
    notebook.add(tab_profile, text="Thông tin cá nhân")
    label_profile = tk.Label(tab_profile, font=("Arial", 14), justify="left")
    label_profile.pack(pady=20)
    load_profile(user_id, label_profile)
    
# Tab 4: Lịch sử mượn
    tab_history = ttk.Frame(notebook)
    notebook.add(tab_history, text="Lịch sử mượn")
    tree_history = ttk.Treeview(tab_history, columns=("Tên sách", "Ngày mượn", "Ngày trả"), show="headings")
    for col in ("Tên sách", "Ngày mượn", "Ngày trả"):
        tree_history.heading(col, text=col)
        tree_history.column(col, width=200)
    tree_history.pack(fill="both", expand=True, padx=10, pady=10)
    load_history(user_id, tree_history)

    tk.Label(window, text="Thư viện", font=("Arial", 16)).pack(pady=5)
    window.mainloop()


def load_books(tree):
    for row in tree.get_children():
        tree.delete(row)
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, title, author FROM books")
    for b in cursor.fetchall():
        tree.insert("", "end", values=b)
    db.close()

def search_books(keyword, tree):
    for row in tree.get_children():
        tree.delete(row)
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, title, author FROM books WHERE title LIKE ? OR author LIKE ?", 
                   (f"%{keyword}%", f"%{keyword}%"))
    for b in cursor.fetchall():
        tree.insert("", "end", values=b)
    db.close()

def load_profile(user_id, label):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, email FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    if user:
        label.config(text=f"Tên: {user[0]}\nEmail: {user[1]}")
    else:
        label.config(text="Không tìm thấy thông tin người dùng.")
    db.close()

def load_history(user_id, tree):
    for row in tree.get_children():
        tree.delete(row)
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT b.title, br.borrow_date, br.return_date
        FROM borrow_records br
        JOIN books b ON br.book_id = b.id
        WHERE br.user_id = ?
    """, (user_id,))
    for r in cursor.fetchall():
        tree.insert("", "end", values=(r[0], r[1], r[2] if r[2] else "Chưa trả"))
    db.close()
    
# Demo
def borrow():
    messagebox.showinfo("Thông báo", "Chức năng mượn sách đang phát triển.")

def return_book():
    messagebox.showinfo("Thông báo", "Chức năng trả sách đang phát triển.")

# Hàm đăng nhập đơn giản để lấy user_id
def login_and_open():
    root = tk.Tk()
    root.withdraw()
    user_id = simpledialog.askinteger("Đăng nhập", "Nhập ID người dùng:")
    if user_id:
        root.destroy()
        open_user_interface(user_id)
    else:
        messagebox.showinfo("Thông báo", "Bạn phải nhập ID để sử dụng.")
        root.destroy()

if __name__ == "__main__":
    login_and_open()

print("File user_interface.py đã được load thành công")