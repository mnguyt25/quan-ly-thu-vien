import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import pyodbc
from datetime import datetime, timedelta

# Kết nối cơ sở dữ liệu
class Database:
    def __init__(self):
        self.server = 'localhost'
        self.database = 'library'
        self.username = 'tv'
        self.password = '12345'
        self.driver = '{ODBC Driver 17 for SQL Server}'

    def connect(self):
        return pyodbc.connect(
            f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
        )

db = Database()

# Lấy ID của user
def get_user_id(username):
    db = Database().connect()
    cursor = db.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    db.close()
    return result[0] if result else None

# Giao diện người dùng chính
def open_user_interface(username):
    window = tk.Tk()
    window.title("Giao diện Người dùng")
    window.geometry("700x500")
    try:
        window.iconbitmap("books_icon.ico")
    except:
        pass

    notebook = ttk.Notebook(window)
    notebook.pack(fill='both', expand=True)

    # === TABS ===
    frame_sach = tk.Frame(notebook)
    frame_muon = tk.Frame(notebook)
    frame_ls = tk.Frame(notebook)

    notebook.add(frame_sach, text='📚 Danh sách sách')
    notebook.add(frame_muon, text='📖 Mượn/Trả sách')
    notebook.add(frame_ls, text='🕓 Lịch sử mượn')

    # ===============================
    # 1. TAB DANH SÁCH SÁCH + TÌM KIẾM
    # ===============================
    tk.Label(frame_sach, text="Tìm kiếm sách theo tên:").pack()
    search_entry = tk.Entry(frame_sach)
    search_entry.pack()

    def load_books(keyword=""):
        for i in tree_books.get_children():
            tree_books.delete(i)

        conn = db.connect()
        cursor = conn.cursor()
        if keyword:
            cursor.execute("SELECT id, ten_sach, tac_gia, so_trang, nam_xuat_ban FROM books WHERE ten_sach LIKE ?", ('%' + keyword + '%',))
        else:
            cursor.execute("SELECT id, ten_sach, tac_gia, so_trang, nam_xuat_ban FROM books")
        for row in cursor.fetchall():
            tree_books.insert("", "end", values=row)
        conn.close()

    tk.Button(frame_sach, text="Tìm", command=lambda: load_books(search_entry.get())).pack()

    columns = ("ID", "Tên sách", "Tác giả", "Số trang", "Năm xuất bản")
    tree_books = ttk.Treeview(frame_sach, columns=columns, show="headings")

    column_configs = [
       ("ID", 50),
       ("Tên sách", 200),
       ("Tác giả", 150),
       ("Số trang", 100),
       ("Năm xuất bản", 120)
     ]

    for col, width in column_configs:
     tree_books.heading(col, text=col)
     tree_books.column(col, width=width, anchor="center")

    tree_books.pack(fill="both", expand=True)

    load_books()

    # ===============================
    # 2. MƯỢN & TRẢ SÁCH
    # ===============================
    def borrow_book():
        print("Đang mượn sách với:", username)
        book_id = simpledialog.askinteger("Mượn sách", "Nhập ID sách muốn mượn:")
        if not book_id:
            return

        today = datetime.now().date()
        try:
            conn = db.connect()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO borrow_records (book_id, username, borrow_date)
                VALUES (?, ?, ?)
            """, (book_id, username, today))
            conn.commit()
            conn.close()
            messagebox.showinfo("Thành công", "Mượn sách thành công!")
            load_borrow_history()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))


    def return_book():
        record_id = simpledialog.askinteger("Trả sách", "Nhập ID lịch sử mượn:")
        if not record_id:
            return

        today = datetime.now().date()
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("UPDATE borrow_records SET return_date = ? WHERE id = ? AND username = ?", (today, record_id, username))
        if cursor.rowcount == 0:
            messagebox.showwarning("Không tìm thấy", "Không có bản ghi phù hợp.")
        else:
            conn.commit()
            messagebox.showinfo("Thành công", "Trả sách thành công!")
            load_borrow_history()
        conn.close()

    tk.Button(frame_muon, text="📥 Mượn sách", command=borrow_book).pack(pady=10)
    tk.Button(frame_muon, text="📤 Trả sách", command=return_book).pack(pady=10)

    # ===============================
    # 3. LỊCH SỬ MƯỢN & GIA HẠN
    # ===============================
    tree_history = ttk.Treeview(frame_ls, columns=("ID", "Tên sách", "Ngày mượn", "Ngày trả"), show="headings")

# Thiết lập tiêu đề và độ rộng cột
    columns = [("ID", 50), ("Tên sách", 250), ("Ngày mượn", 120), ("Ngày trả", 120)]
    for col, width in columns:
     tree_history.heading(col, text=col)
     tree_history.column(col, width=width, anchor="center")

    tree_history.pack(fill="both", expand=True)


    def load_borrow_history():
     for i in tree_history.get_children():
        tree_history.delete(i)

     conn = db.connect()
     cursor = conn.cursor()
     cursor.execute("""
        SELECT br.id, b.ten_sach, br.borrow_date, br.return_date
        FROM borrow_records br
        JOIN books b ON br.book_id = b.id
        WHERE br.username = ?
    """, (username,))

     for row in cursor.fetchall():
        id_val, ten_sach, borrow_date, return_date = row

        # Chuyển định dạng ngày nếu không phải None
        borrow_str = borrow_date.strftime("%d/%m/%Y") if borrow_date else ""
        return_str = return_date.strftime("%d/%m/%Y") if return_date else ""

        tree_history.insert("", "end", values=(id_val, ten_sach, borrow_str, return_str))

     conn.close()


    def renew_book():
        selected = tree_history.focus()
        if not selected:
          messagebox.showwarning("Chọn sách", "Vui lòng chọn dòng cần gia hạn.")
          return

        try:
          renew_days = int(renew_days_entry.get())
          if renew_days <= 0:
            raise ValueError
        except ValueError:
           messagebox.showwarning("Lỗi", "Vui lòng nhập số ngày hợp lệ (lớn hơn 0).")
           return

        record_id = tree_history.item(selected)['values'][0]

        conn = db.connect()
        cursor = conn.cursor()

    # Lấy ngày trả hiện tại
        cursor.execute("SELECT return_date FROM borrow_records WHERE id = ?", (record_id,))
        row = cursor.fetchone()
        if not row or not row[0]:
          messagebox.showerror("Lỗi", "Không tìm thấy ngày trả để gia hạn.")
          conn.close()
          return

        
        current_return_date = row[0]
        new_return_date = current_return_date + timedelta(days=renew_days)

    # Cập nhật ngày trả mới
        cursor.execute("UPDATE borrow_records SET return_date = ? WHERE id = ?", 
                   (new_return_date.strftime("%Y-%m-%d"), record_id))

    # Ghi log gia hạn
        cursor.execute("INSERT INTO renew_logs (borrow_id, note) VALUES (?, ?)", 
                   (record_id, f"Gia hạn thêm {renew_days} ngày"))

        conn.commit()
        conn.close()

        messagebox.showinfo("Thành công", f"Gia hạn thành công thêm {renew_days} ngày!")
        load_borrow_history()


    tk.Label(frame_ls, text="Số ngày muốn gia hạn:").pack()
    renew_days_entry = tk.Entry(frame_ls)
    renew_days_entry.pack()
    tk.Button(frame_ls, text="🔁 Gia hạn sách", command=renew_book).pack(pady=10)
    load_borrow_history()

    window.mainloop()
