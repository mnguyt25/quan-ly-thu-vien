import tkinter as tk
from tkinter import messagebox, ttk
from database import Database
from datetime import date

# =================== Mượn và Trả sách ===================
def borrow_book():
    top = tk.Toplevel()
    top.title("Mượn sách")

    tk.Label(top, text="ID người dùng:").grid(row=0, column=0, padx=10, pady=5)
    user_entry = tk.Entry(top)
    user_entry.grid(row=0, column=1)

    tk.Label(top, text="ID sách:").grid(row=1, column=0, padx=10, pady=5)
    book_entry = tk.Entry(top)
    book_entry.grid(row=1, column=1)

    def borrow():
        user_id = user_entry.get()
        book_id = book_entry.get()

        if not (user_id.isdigit() and book_id.isdigit()):
            messagebox.showerror("Lỗi", "ID phải là số.")
            return

        db = Database()
        book = db.fetch_one("SELECT trang_thai FROM books WHERE id = %s", (book_id,))
        if not book:
            messagebox.showerror("Lỗi", "Sách không tồn tại.")
            return
        if book[0] != 0:
            messagebox.showerror("Lỗi", "Sách đang được mượn.")
            return

        db.execute_query("UPDATE books SET trang_thai = %s WHERE id = %s", ("1", book_id))
        messagebox.showinfo("Thành công", "Đã mượn sách.")
        top.destroy()

    tk.Button(top, text="Mượn", command=borrow).grid(row=2, columnspan=2, pady=10)

def return_book():
    top = tk.Toplevel()
    top.title("Trả sách")

    tk.Label(top, text="ID sách:").grid(row=0, column=0, padx=10, pady=5)
    book_entry = tk.Entry(top)
    book_entry.grid(row=0, column=1)

    def return_bk():
        book_id = book_entry.get()
        if not book_id.isdigit():
            messagebox.showerror("Lỗi", "ID không hợp lệ.")
            return

        db = Database()
        db.execute_query("UPDATE books SET trang_thai = %s WHERE id = %s", ("0", book_id))
        messagebox.showinfo("Thành công", "Đã trả sách.")
        top.destroy()

    tk.Button(top, text="Trả", command=return_bk).grid(row=1, columnspan=2, pady=10)

def show_overdue_books():
    top = tk.Toplevel()
    top.title("Sách quá hạn")
    top.geometry("900x400")

    columns = ("ID Sách", "Tên sách", "Người mượn", "Ngày mượn", "Hạn trả")
    tree = ttk.Treeview(top, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.pack(fill=tk.BOTH, expand=True)

    db = Database()
    today = date.today()

    query = """
        SELECT b.id, b.ten_sach, m.ten_thanh_vien, br.ngay_muon, br.han_tra
        FROM borrowings br
        JOIN books b ON br.id_sach = b.id
        JOIN members m ON br.id_thanh_vien = m.id
        WHERE br.ngay_tra IS NULL AND br.han_tra < %s AND b.trang_thai = 1
    """

    results = db.fetch_all(query, (today,))

    for row in results:
        tree.insert("", tk.END, values=row)