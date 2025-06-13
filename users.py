import tkinter as tk
from tkinter import messagebox, ttk
from database import Database

# =================== Chức năng Người dùng ===================

def add_user():
    top = tk.Toplevel()
    top.title("Thêm người dùng")

    tk.Label(top, text="Tên đăng nhập:").grid(row=0, column=0, padx=10, pady=5)
    username_entry = tk.Entry(top)
    username_entry.grid(row=0, column=1)

    tk.Label(top, text="Mật khẩu:").grid(row=1, column=0, padx=10, pady=5)
    password_entry = tk.Entry(top, show="*")
    password_entry.grid(row=1, column=1)

    tk.Label(top, text="Vai trò:").grid(row=2, column=0, padx=10, pady=5)
    role_cb = ttk.Combobox(top, values=["public", "admin"])
    role_cb.current(0)
    role_cb.grid(row=2, column=1)

    def insert_user():
        username = username_entry.get()
        password = password_entry.get()
        role = role_cb.get()

        if not all([username, password, role]):
            messagebox.showerror("Lỗi", "Nhập đầy đủ thông tin.")
            return

        db = Database()

        # Kiểm tra tên đăng nhập đã tồn tại chưa
        existing = db.fetch_one("SELECT * FROM users WHERE username = %s", (username,))
        if existing:
            messagebox.showerror("Lỗi", "Tên đăng nhập đã tồn tại.")
            return

        # Thêm vào bảng users
        db.execute_query("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", 
                         (username, password, role))
        
        # Đồng thời thêm vào bảng members
        db.execute_query("INSERT INTO members (ten_thanh_vien) VALUES (%s)", (username,))

        messagebox.showinfo("Thành công", "Đã thêm người dùng.")
        top.destroy()

    tk.Button(top, text="Thêm", command=insert_user).grid(row=3, columnspan=2, pady=10)


def edit_user():
    top = tk.Toplevel()
    top.title("Sửa người dùng")

    tk.Label(top, text="Tên đăng nhập cần sửa:").grid(row=0, column=0, padx=10, pady=5)
    username_entry = tk.Entry(top)
    username_entry.grid(row=0, column=1)

    tk.Label(top, text="Mật khẩu mới:").grid(row=1, column=0, padx=10, pady=5)
    password_entry = tk.Entry(top, show="*")
    password_entry.grid(row=1, column=1)

    tk.Label(top, text="Vai trò mới:").grid(row=2, column=0, padx=10, pady=5)
    role_cb = ttk.Combobox(top, values=["admin", "public"])
    role_cb.grid(row=2, column=1)

    def perform_update():
        username = username_entry.get()
        password = password_entry.get()
        role = role_cb.get()

        if not all([username, password, role]):
            messagebox.showerror("Lỗi", "Vui lòng điền đầy đủ thông tin.")
            return
        if role not in ("admin", "public"):
            messagebox.showerror("Lỗi", "Vai trò không hợp lệ.")
            return

        db = Database()
        user = db.fetch_one("SELECT * FROM users WHERE username = %s", (username,))
        if user:
            query = "UPDATE users SET password=%s, role=%s WHERE username=%s"
            db.execute_query(query, (password, role, username))
            messagebox.showinfo("Thành công", "Đã cập nhật người dùng.")
            top.destroy()
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy người dùng.")

    tk.Button(top, text="Cập nhật", command=perform_update).grid(row=3, columnspan=2, pady=10)

def delete_user():
    top = tk.Toplevel()
    top.title("Xóa người dùng")

    tk.Label(top, text="Tên đăng nhập cần xóa:").grid(row=0, column=0, padx=10, pady=5)
    username_entry = tk.Entry(top)
    username_entry.grid(row=0, column=1)

    def perform_delete():
        username = username_entry.get()
        if not username:
            messagebox.showerror("Lỗi", "Vui lòng nhập tên đăng nhập.")
            return

        db = Database()
        user = db.fetch_one("SELECT * FROM users WHERE username = %s", (username,))
        if user:
            confirm = messagebox.askyesno("Xác nhận", f"Bạn có chắc chắn muốn xóa người dùng '{username}'?")
            if confirm:
                db.execute_query("DELETE FROM users WHERE username = %s", (username,))
                messagebox.showinfo("Thành công", f"Đã xóa người dùng '{username}'.")
                top.destroy()
        else:
            messagebox.showerror("Lỗi", "Không tìm thấy người dùng.")

    tk.Button(top, text="Xóa", command=perform_delete).grid(row=1, columnspan=2, pady=10)

def find_user():
    top = tk.Toplevel()
    top.title("Tìm người dùng")

    tk.Label(top, text="Nhập tên người dùng:").pack()
    keyword_entry = tk.Entry(top)
    keyword_entry.pack()

    tree = ttk.Treeview(top, columns=("Tên", "Mật khẩu"), show="headings")
    tree.heading("Tên", text="Tên")
    tree.heading("Mật khẩu", text="Mật khẩu")
    tree.column("Tên", width=150)
    tree.column("Mật khẩu", width=150)
    tree.pack(fill=tk.BOTH, expand=True)

    def search():
        keyword = keyword_entry.get()
        db = Database()
        query = "SELECT ten, mat_khau FROM users WHERE ten LIKE %s"
        results = db.fetch_all(query, (f"%{keyword}%",))

        for row in tree.get_children():
            tree.delete(row)

        for r in results:
            tree.insert("", tk.END, values=r)

    tk.Button(top, text="Tìm", command=search).pack(pady=5)
def show_user():
    top = tk.Toplevel()
    top.title("Danh sách người dùng")
    top.geometry("600x400")

    columns = ("ID", "Tên thành viên")
    tree = ttk.Treeview(top, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)

    tree.pack(fill=tk.BOTH, expand=True)

    db = Database()
    members = db.fetch_all("SELECT * FROM members ORDER BY id ASC")

    for member in members:
        tree.insert("", tk.END, values=member)