import tkinter as tk
from tkinter import messagebox, ttk
from database import Database

# ====================== Chức năng Sách ======================
def add_book():
    top = tk.Toplevel()
    top.title("Thêm sách")
    labels = ["Tên sách", "Tác giả", "Số trang", "Năm xuất bản", "Trạng thái", "Chủng loại"]
    entries = []

    for i, label in enumerate(labels):
        tk.Label(top, text=label + ":").grid(row=i, column=0, padx=10, pady=5)
        if label == "Chủng loại":
            cb = ttk.Combobox(top, values=["Truyện ngắn", "Tiểu thuyết", "Giáo trình", "Tài liệu", "Khác"])
            cb.grid(row=i, column=1, padx=10, pady=5)
            entries.append(cb)
        elif label == "Trạng thái":
            cb = ttk.Combobox(top, values=["0 - Có", "1 - Mượn", "2 - Khác"])
            cb.grid(row=i, column=1, padx=10, pady=5)
            entries.append(cb)
        else:
            entry = tk.Entry(top)
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries.append(entry)

    def insert_book():
        values = [entry.get() for entry in entries]
        if not all(values):
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")
            return

        db = Database()
        query = """INSERT INTO books (ten_sach, tac_gia, so_trang, nam_xuat_ban, trang_thai, chung_loai)
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        db.execute_query(query, tuple(values))
        messagebox.showinfo("Thành công", "Đã thêm sách.")
        top.destroy()

    tk.Button(top, text="Thêm sách", command=insert_book).grid(row=len(labels), columnspan=2, pady=10)

def edit_book():
    top = tk.Toplevel()
    top.title("Sửa sách")

    tk.Label(top, text="Nhập ID sách:").grid(row=0, column=0, padx=10, pady=5)
    id_entry = tk.Entry(top)
    id_entry.grid(row=0, column=1)

    def search_and_edit():
        book_id = id_entry.get()
        if not book_id.isdigit():
            messagebox.showerror("Lỗi", "ID không hợp lệ.")
            return

        db = Database()
        result = db.fetch_one("SELECT * FROM books WHERE id = %s", (book_id,))
        if not result:
            messagebox.showerror("Không tìm thấy", "Không tìm thấy sách.")
            return

        labels = ["Tên sách", "Tác giả", "Số trang", "Năm xuất bản", "Trạng thái", "Chủng loại"]
        entries = []
        for i, label in enumerate(labels):
            tk.Label(top, text=label + ":").grid(row=i+1, column=0, padx=10, pady=5)
            if label == "Trạng thái":
                cb = ttk.Combobox(top, values=["0 - Có", "1 - Mượn", "2 - Khác"])
                cb.set(str(result[5]))
                cb.grid(row=i+1, column=1)
                entries.append(cb)
            elif label == "Chủng loại":
                cb = ttk.Combobox(top, values=["Truyện ngắn", "Tiểu thuyết", "Giáo trình", "Tài liệu", "Khác"])
                cb.set(result[6])
                cb.grid(row=i+1, column=1)
                entries.append(cb)
            else:
                entry = tk.Entry(top)
                entry.insert(0, result[i+1])
                entry.grid(row=i+1, column=1)
                entries.append(entry)

        def update_book():
            new_values = [e.get() for e in entries]
            if not all(new_values):
                messagebox.showerror("Lỗi", "Vui lòng điền đủ thông tin.")
                return

            query = """UPDATE books 
                       SET ten_sach=%s, tac_gia=%s, so_trang=%s, nam_xuat_ban=%s, trang_thai=%s, chung_loai=%s
                       WHERE id=%s"""
            db.execute_query(query, (*new_values, book_id))
            messagebox.showinfo("Thành công", "Đã cập nhật sách.")
            top.destroy()

        tk.Button(top, text="Cập nhật", command=update_book).grid(row=len(labels)+1, columnspan=2, pady=10)

    tk.Button(top, text="Tìm & Sửa", command=search_and_edit).grid(row=0, column=2, padx=5)

def delete_book():
    top = tk.Toplevel()
    top.title("Xóa sách")

    tk.Label(top, text="Nhập ID sách cần xóa:").pack()
    id_entry = tk.Entry(top)
    id_entry.pack()

    def perform_delete():
        book_id = id_entry.get()
        if not book_id.isdigit():
            messagebox.showerror("Lỗi", "ID không hợp lệ.")
            return

        db = Database()
        db.execute_query("DELETE FROM books WHERE id = %s", (book_id,))
        messagebox.showinfo("Thành công", "Đã xóa sách.")
        top.destroy()

    tk.Button(top, text="Xóa", command=perform_delete).pack()

def find_book():
    top = tk.Toplevel()
    top.title("Tìm sách")
    tk.Label(top, text="Từ khóa tìm kiếm:").pack()
    keyword_entry = tk.Entry(top)
    keyword_entry.pack()

    tree = ttk.Treeview(top, columns=("id", "Tên sách", "Tác giả", "Số trang", "Năm xuất bản", "Trạng thái", "Chủng loại"), show="headings")
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(fill=tk.BOTH, expand=True)

    def search():
        keyword = keyword_entry.get()
        db = Database()
        query = """SELECT * FROM books 
                   WHERE ten_sach LIKE %s OR tac_gia LIKE %s OR chung_loai LIKE %s"""
        results = db.fetch_all(query, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))

        for row in tree.get_children():
            tree.delete(row)

        for r in results:
            tree.insert("", tk.END, values=r)

    tk.Button(top, text="Tìm", command=search).pack(pady=5)

def show_book():
    top = tk.Toplevel()
    top.title("Danh sách sách")
    top.geometry("800x400")

    columns = ("id", "Tên sách", "Tác giả", "Số trang", "Năm xuất bản", "Trạng thái", "Chủng loại")
    tree = ttk.Treeview(top, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    tree.pack(fill=tk.BOTH, expand=True)

    db = Database()
    books = db.fetch_all("SELECT * FROM books")

    for book in books:
        tree.insert("", tk.END, values=book)
